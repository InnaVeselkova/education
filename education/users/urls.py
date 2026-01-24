from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserProfileEditView, PaymentListCreateView, UserRegisterView, UserListView, UserDetailView, \
    UserDeleteView, PaymentSuccessView, PaymentCancelView
from .views import CustomAuthToken
from .views import MyTokenObtainPairView

app_name='users'

urlpatterns = [
    path('profile/edit/', UserProfileEditView.as_view(), name='user_edit'),
    path('users/', UserListView.as_view(), name='user-list'),  # Список пользователей
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Детальный просмотр пользователя
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),  # Удаление пользователя
    path('payments/', PaymentListCreateView.as_view(), name='payment_list_create'),
    path('token-auth/', CustomAuthToken.as_view(), name='token_auth'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),# Эндпоинт для получения токена
    path('register/', UserRegisterView.as_view(), name='user-register'), # Эндпоинт для регистрации пользователя
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('payment-cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
]
