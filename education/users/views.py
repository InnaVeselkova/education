from django.shortcuts import redirect
from django.views.generic import TemplateView
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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_course', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        course_id = data.get('paid_course')
        if not course_id:
            return Response({"detail": "Не указан paid_course."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Курс не найден."}, status=status.HTTP_404_NOT_FOUND)

        payment_method = data.get('payment_method')

        if payment_method == "stripe":
            # Создаем платеж
            payment = Payment.objects.create(
                user=request.user,
                paid_course=course,
                payment_method='stripe',
            )
            try:
                session_data = init_stripe_payment(
                    payment,
                    success_url=request.build_absolute_uri('/payment-success/'),
                    cancel_url = request.build_absolute_uri('/payment-cancel/')
                )
            except Exception as e:
                payment.delete()
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Перенаправляем на Stripe
            return redirect(session_data['url'])

        elif payment_method in ("cash", "transfer"):
            if 'amount' not in data:
                data['amount'] = str(course.price)
            return super().create(request, *args, **kwargs)

        else:
            return Response({"detail": "Неподдерживаемый payment_method."}, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user, owner=self.request.user)


class PaymentSuccessView(TemplateView):
    template_name = 'payments/success.html'


class PaymentCancelView(TemplateView):
    template_name = 'payments/cancel.html'

