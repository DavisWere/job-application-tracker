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


class JobSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Job
        fields = ['id', 'user', 'job_title', 'job_description', 'date_posted']

    def validate(self, data):
        user = data.get('user')
        if user.user_type != 'employer':
            raise serializers.ValidationError(
                'Only employers can upload job/s')
        return super().validate(data)

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        job = Job.objects.create(**validated_data)
        job.save()
        return job

    def update(self, instance, validated_data):
        user = validated_data.pop('user', None)
        job = super().update(instance, validated_data)
        job.save()
        if user is not None:
            instance.user = user
        instance.save()
        return instance
