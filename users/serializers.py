from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

class UserCreateSerializer(UserCreateSerializer):
  class Meta:
    model = get_user_model()
    fields = ('id', 'email', 'first_name', 'last_name', 'password')