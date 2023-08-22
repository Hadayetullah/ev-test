from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Dashboard

from . import serializers
from app_auth import renderers

# Create your views here.


class UserInputView(APIView):
    # renderer_classes = [renderers.UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = serializers.UserInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            array_value = serializer.data.get('array_value')
            numbers = [int(num.strip()) for num in array_value.replace(
                " ", "").split(',') if num.strip()]
            sorted_numbers = sorted(numbers, reverse=True)
            sorted_string = ", ".join(str(num) for num in sorted_numbers)
            search_value = serializer.validated_data.pop('search_value', None)

            dashboard_instance = Dashboard(**serializer.validated_data)
            dashboard_instance.array_value = sorted_string
            dashboard_instance.save()

            if search_value in sorted_numbers:
                search_value = True
            else:
                search_value = False

            return Response({'result': search_value}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
