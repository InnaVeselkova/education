from django.urls import path
from .views import UserProfileEditView

app_name='users'

urlpatterns = [
    path('profile/edit/', UserProfileEditView.as_view(), name='user_edit'),
]