from rest_framework import serializers
from app_dashboard import models


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dashboard
        fields = '__all__'


class PayloadSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    input_values = serializers.CharField()


class ResponseSerializer(serializers.Serializer):
    status = serializers.CharField(default='success')
    user_id = serializers.IntegerField(source='user.id')
    payload = PayloadSerializer(many=True)
