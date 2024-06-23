import django_filters
from core.models import User, Job, Payment


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'first_name': ['icontains'],
            'second_name': ['icontains'],
            'phone_number': ['icontains'],
            'email': ['icontains'],
            'username': ['icontains'],
            'user_type': ['exact'],
        }


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            'job_title': ['icontains'],
            'date_posted': ['icontains'],
            'job_description': ['icontains']
        }


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'user': ['exact'],
            'amount': ['exact'],
            'payment_method': ['exact']
        }
