from rest_framework import generics, permissions, viewsets
from .serializers import UserSerializer


class UserProfileEditView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
