from rest_framework import serializers
from .models import Sending, Message, ClientFilter
from apps.clientstuff.serializers import ClientSerializer

class ClientFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientFilter
        fields = ('tag','mob_operator_code')

class SendingSerializer(serializers.ModelSerializer):
    client_filter = ClientFilterSerializer()
    class Meta:
        model = Sending
        fields = ('id','start_date','end_date','message_text','client_filter')

    def create(self, validated_data):
        client_filter = validated_data.pop('client_filter')

        client_filter_instance, _ = ClientFilter.objects.get_or_create(**client_filter)

        try:
            sending = Sending.objects.create(client_filter=client_filter_instance,**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(
                {'errors':[e]}
            )
        
        return sending

    def update(self, instance: Sending, validated_data):
        client_filter = validated_data.get('client_filter')
        
        if client_filter:
            client_filter_instance, _ = ClientFilter.objects.get_or_create(**client_filter)
            validated_data['client_filter'] = client_filter_instance
        
        for key, value in validated_data.items():
            setattr(instance,key, value)
            
        try:
            instance.save()
        except ValueError as e:
            raise serializers.ValidationError(
                {'errors':[e]}
            )
        
        return instance



class MessageSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    send_status = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id','send_status','created_date','client')
        depth = 1
    
    def get_send_status(self, obj):
        return obj.get_send_status_display()

class SendingGeneralInfoSerializer(serializers.ModelSerializer):
    total_messages = serializers.IntegerField()
    sent = serializers.IntegerField()
    error = serializers.IntegerField()
    created = serializers.IntegerField()
    class Meta:
        model = Sending
        fields = ( 'id', 'total_messages', 'sent', 'error', 'created','message_text')

class SendingInfoSerializer(serializers.ModelSerializer):
    total_messages = serializers.IntegerField()
    sent = serializers.IntegerField()
    error = serializers.IntegerField()
    created = serializers.IntegerField()
    client_filter = ClientFilterSerializer()
    messages = MessageSerializer(many=True)
    class Meta:
        model = Sending
        fields = (
            'id','message_text','start_date','end_date',
            'client_filter', 'total_messages', 'sent','error',
            'created','messages'
        )