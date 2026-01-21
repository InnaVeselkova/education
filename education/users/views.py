from rest_framework import generics, permissions, viewsets, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, User
from .serializers import UserSerializer, PaymentSerializer, MyTokenObtainPairSerializer, UserRegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from education_app.models import Course

from .stripe_service import init_stripe_payment


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class UserProfileEditView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Добавление проверки авторизации


    def get_object(self):
        return self.request.user


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Разрешить регистрация для всех

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Сохранить пользователя
            return Response({
                "user": UserSerializer(user).data,
                "message": "Пользователь успешно зарегистрирован."
            }, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    query_set = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['paid_course', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        method = data.get('payment_method')
        course_id = data.get('paid_course')

        # Проверка наличия курса
        if not course_id:
            return Response(
                {"detail": "Не указан paid_course."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Курс не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Обработка Stripe
        if method == "stripe":
            required_fields = ['success_url', 'cancel_url']
            for field in required_fields:
                if not data.get(field):
                    return Response(
                        {"detail": f"Требуется {field}."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            success_url = data.get('success_url')
            cancel_url = data.get('cancel_url')

            # Создаём платеж через Stripe
            try:
                payment = init_stripe_payment(
                    user=request.user,
                    course=course,
                    success_url=success_url,
                    cancel_url=cancel_url
                )
            except Exception as e:
                return Response(
                    {"detail": f"Ошибка при создании платежа: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            serializer = self.get_serializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Для cash / transfer
        elif method in ("cash", "transfer"):
            # Устанавливаем сумму (если не указана явно)
            if 'amount' not in data:
                data['amount'] = str(course.price)
            # Передача данных в суперметод для сохранения
            return super().create(request, *args, **kwargs)

        # Если метод не поддерживается
        else:
            return Response(
                {"detail": "Неподдерживаемый payment_method."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, owner=self.request.user)

