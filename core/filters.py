import django_filters
from core.models import User


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
