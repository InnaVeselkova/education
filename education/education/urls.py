from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("education_app.urls", namespace='education_app')),
    path("users/", include("users.urls", namespace='users')),
]
