from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import UserProfileEditView, PaymentListCreateView, UserRegisterView
from .views import CustomAuthToken
from .views import MyTokenObtainPairView

app_name='users'

urlpatterns = [
    path('profile/edit/', UserProfileEditView.as_view(), name='user_edit'),
    path('payments/', PaymentListCreateView.as_view(), name='payment_list_create'),
    path('token-auth/', CustomAuthToken.as_view(), name='token_auth'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),# Эндпоинт для получения токена
    path('register/', UserRegisterView.as_view(), name='user-register'), # Эндпоинт для регистрации пользователя
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Эндпоинт для обновления токена
]
