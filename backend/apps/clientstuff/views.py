from rest_framework.permissions import AllowAny
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView
from .models import Client
from .serializers import ClientSerializer
from rest_framework import status
from rest_framework.response import Response

class CreateClientView(CreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = (AllowAny, )

class DestroyUpdateClientView(UpdateAPIView, DestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (AllowAny, )
    lookup_field = 'phone_number'
    def put(self, request, phone_number=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)