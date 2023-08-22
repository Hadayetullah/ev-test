from django.contrib.auth import authenticate
from datetime import datetime, timezone

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from app_dashboard.models import Dashboard

from . import serializers
from app_auth import renderers


class UserDataView(APIView):
    # renderer_classes = [renderers.UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, start, end, format=None):
        user = request.user
        start_date = datetime.strptime(
            start, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(
            end, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)

        print(start_date)
        # Filtered the Dashboard instances based on the range of dates
        dashboards = Dashboard.objects.filter(
            user=user, created_at__range=(start_date, end_date))

        # print(dashboard)

        payload_data = []
        for dashboard in dashboards:
            payload_data.append({
                'timestamp': dashboard.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'input_values': dashboard.array_value
            })

        response_data = {
            'status': 'success',
            'user_id': user.id,
            'payload': payload_data
        }

        serializer = serializers.ResponseSerializer(data=response_data)
        serializer.is_valid()

        return Response(serializer.validated_data)
        # return Response(serializer.data, status=status.HTTP_200_OK)
