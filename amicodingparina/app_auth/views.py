from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from app_auth import renderers
from . import serializers
from . import models

# Create your views here.

# Creating tokens manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    # renderer_classes = [renderers.UserRenderer]

    def post(self, request, format=None):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': "A verification mail has been sent to your email. Please check your email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationVarificationView(APIView):
    # renderer_classes = [renderers.UserRenderer]
    def get(self, request, uid, user_token, format=None):
        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = models.User.objects.get(pk=id)
            token_obj = models.Token.objects.get(user=user)

            if token_obj is not None:
                if token_obj.is_valid:
                    if default_token_generator.check_token(user, user_token):
                        user.is_active = True
                        user_obj = user
                        user.save()
                        token = get_tokens_for_user(user_obj)
                        return Response({"token": token, "msg": "Varification Successfull"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other exceptions here, and return an appropriate response
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):
    renderer_classes = [renderers.UserRenderer]

    def post(self, request, format=None):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':
                                 {'non_field_errors':
                                  ['Email or password is not valid']}
                                 },
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserDashboardView(APIView):
#     # renderer_classes = [renderers.UserRenderer]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         serializer = serializers.UserDashboardSerializer(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
