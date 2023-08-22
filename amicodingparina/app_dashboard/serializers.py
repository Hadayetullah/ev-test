import re
from rest_framework import serializers
from . import models


class UserInputSerializer(serializers.ModelSerializer):
    search_value = serializers.IntegerField()

    class Meta:
        model = models.Dashboard
        fields = ['user', 'array_value', 'search_value']

    def validate(self, attrs):
        array_value = attrs.get('array_value')
        search_value = attrs.get('search_value')

        values = array_value.split(',')
        for value in values:
            if not re.match(r'\s*\d+\s*', value):
                raise serializers.ValidationError("Invalid Input")

        try:
            search_value = int(search_value)
        except ValueError:
            serializers.ValidationError("Input value must be an integer")

        return attrs
