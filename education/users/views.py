from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import UserSerializer, PaymentSerializer, MyTokenObtainPairSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

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


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        'paid_course': 'paid_course',  # Фильтрация по курсу
        'paid_lesson': 'paid_lesson',  # Фильтрация по уроку
        'payment_method': 'payment_method',  # Фильтрация по методу оплаты
    }
    ordering_fields = ['payment_date']  # Поля для сортировки
    ordering = ['payment_date']
    permission_classes = [permissions.IsAuthenticated]
