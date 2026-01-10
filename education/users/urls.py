from django.urls import path
from .views import UserProfileEditView, PaymentListCreateView
from .views import CustomAuthToken

app_name='users'

urlpatterns = [
    path('profile/edit/', UserProfileEditView.as_view(), name='user_edit'),
    path('payments/', PaymentListCreateView.as_view(), name='payment_list_create'),
    path('token-auth/', CustomAuthToken.as_view(), name='token_auth'),
]
