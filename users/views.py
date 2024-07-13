from rest_framework.views import APIView
from rest_framework.response import Response
from djoser.serializers import UserSerializer
from .models import UserAccount


class ListUsers(APIView):
  def get(self, request, is_staff=None):
    if is_staff is None:
      users = UserAccount.objects.all()
    elif is_staff:
      users = UserAccount.objects.filter(is_staff=True)
    else:
      users = UserAccount.objects.filter(is_staff=False)


    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


class ListCustomers(ListUsers):
  def get(self, request):
    return super().get(request, is_staff=False)

class ListAdminUsers(ListUsers):
  def get(self, request):
    return super().get(request, is_staff=True)


#address views missing
