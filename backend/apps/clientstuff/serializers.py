from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

    
    def create(self, validated_data):
        try:
            return Client.objects.create(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(
                {'errors':[e]}
            )
        
    def update(self, instance: Client, validated_data):
        for key, value in validated_data.items():
            setattr(instance,key, value)
            
        try:
            instance.save()
        except ValueError as e:
            raise serializers.ValidationError(
                {'errors':[e]}
            )
        
        return instance