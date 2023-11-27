from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Case, When, Value, Prefetch
from django.db.models.functions import Coalesce
from .serializers import SendingGeneralInfoSerializer, SendingInfoSerializer, SendingSerializer
from .models import Sending, Message
from django.utils import timezone
from django.http import JsonResponse
import json


class CreateListSendingView(ViewSet):
    serializer_class = SendingSerializer
    permission_classes = (AllowAny, )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, reuest):
        sending_info = Sending.objects.prefetch_related(
            Prefetch(
                'message_set',
                queryset=Message.objects.order_by('send_status'),
                to_attr='messages'
            ),
            'client_filter'
        ).annotate(
            total_messages=Count('message'),
            sent=Coalesce(Sum(Case(When(message__send_status=Message.SendStatus.SENT, then=1))), Value(0)),
            error=Coalesce(Sum(Case(When(message__send_status=Message.SendStatus.ERROR, then=1))), Value(0)),
            created=Coalesce(Sum(Case(When(message__send_status=Message.SendStatus.CREATED, then=1))), Value(0)),
        )
        serializer = SendingGeneralInfoSerializer(sending_info, many=True)

        return Response(serializer.data)

class RetrieveUpdateDestroySendingView(RetrieveUpdateDestroyAPIView):
    serializer_class = SendingSerializer
    permission_classes = (AllowAny, )
    queryset = Sending.objects.all()
    lookup_field = 'pk'

    def get(self, request, pk=None):

        sending_info = Sending.objects.filter(id=pk).prefetch_related(
            Prefetch(
                'message_set',
                queryset=Message.objects.order_by('send_status'),
                to_attr='messages'
            ),
            'client_filter'
        ).annotate(
            total_messages=Count('message'),
            sent=Coalesce(Sum(Case(When(message__send_status=Message.SendStatus.SENT, then=1))), Value(0)),
            error=Coalesce(Sum(Case(When(message__send_status=Message.SendStatus.ERROR, then=1))), Value(0)),
            created=Coalesce(Sum(Case(When(message__send_status=Message.SendStatus.CREATED, then=1))), Value(0)),
        )
        if not sending_info.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = SendingInfoSerializer(sending_info.first())

        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        instance: Sending = self.get_object()

        if instance.start_date <= timezone.now():
            return Response(data={'errors':'Нельзя обновить рассылку, пока она активна или закончена'},status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def openapi_spec(request):
    with open('apiSpec.json')as f:
        openapi = json.load(f)

    return JsonResponse(openapi,safe=False)