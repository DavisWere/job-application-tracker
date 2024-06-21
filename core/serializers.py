from datetime import timedelta
from django.utils.timezone import make_aware
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import *


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_superuser"] = user.is_superuser
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'second_name',
                  'phone_number', 'email', 'username', 'password', 'user_type', 'resume']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password')
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_type = self.context['request'].data.get('user_type', None)
        if user_type == 'applicant':
            self.fields['resume'] = serializers.FileField()
