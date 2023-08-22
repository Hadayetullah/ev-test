from rest_framework import serializers
from django.utils import timezone

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator

from . import models
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = models.User
        fields = ['name', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {
                "write_only": True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and confirm password doesn't match")
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        token = models.Token.objects.create(
            user=user, expires_at=timezone.now() + timezone.timedelta(minutes=50))
        token.save()
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token_generator = default_token_generator.make_token(user)
        link = 'http://localhost:5173/authenticate/' + uid + "/" + token_generator
        # print("Token Link: ", link)
        # Send Email
        body = '<h5 style="font-size:18px;font-weight:bold">Click the below button for verification</h5>' + \
            '<div style="width:100%;"><a style="background:#606060;display:inline-block;margin-left:10%;color:white;font-size:18px;font-weight:bold;cursor:pointer;padding:12px 20px 8px;text-decoration:none;border-radius:3px;" href="' + \
            link + '"><span style="line-height:24px;">Confirm</span></a></div>'
        data = {
            'subject': 'User Verification',
            'body': body,
            'to_email': user.email
        }
        Util.send_email(data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = models.User
        fields = ["email", "password"]
