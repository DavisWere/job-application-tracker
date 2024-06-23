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


class PaymentSertializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_method', 'currency', 'amount']

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        payment = Payment.objects.create(user=user, **validated_data)
        payment.save()
        return payment


class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Job.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), required=False)
    payment = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Payment.objects.all(), required=False)

    class Meta:
        model = Application
        fields = ['id', 'user', 'job', 'payment',
                  'applied', 'application_date']

    def create(self, validated_data):
        job = validated_data.pop('job', None)
        user = validated_data.pop('user', None)
        payment = validated_data.pop('payment', None)
        applied = validated_data.get('applied', None)
        if job and user and payment is not None:
            if payment.amount == 1000:
                applied = True
            else:
                applied = False
        application = Application.objects.create(
            job=job, user=user, payment=payment, applied=applied, **validated_data)
        application.save()
        return application

    def update(self, instance, validated_data):
        job = validated_data.pop('job', None)
        user = validated_data.pop('user', None)
        payment = validated_data.pop('payment', None)
        applied = validated_data.get('applied', None)
        application = super().update(instance, validated_data)
        application.save()
        if job is not None:
            instance.job = job
        if user is not None:
            instance.user = user
        if payment is not None:
            instance.payment = payment
        if applied is not None:
            instance.applied = applied
        instance.save()
        return instance
