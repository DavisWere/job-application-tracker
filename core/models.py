from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.


class User(AbstractUser):
    USER_TYPES = [
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
    ]
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=1000, null=False)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPES, default='applicant')

    def __str__(self):
        return f"{self.first_name} {self.second_name}"


class Jobs(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    job_description = models.TextField(max_length=500, null=True, blank=True)
    date_posted = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.job_title}"


class Currency(models.TextChoices):
    SH = 'sh', 'Shilling'
    TSH = 'tsh', 'Tanzanian Shilling'
    USD = 'usd', 'US Dollar'


class PaymentMethod(models.TextChoices):
    MPESA = 'mpesa', 'M-Pesa'
    PAYPAL = 'paypal', 'PayPal'
    VISA = 'visa', 'Visa'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.MPESA
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.SH
    )
    amount = models.FloatField(null=True)

    def __str__(self):
        return f"Payment ID: {self.id} - User: {self.user} - Method: {self.payment_method} - Currency: {self.currency}"


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, null=True)
    applied = models.BooleanField(default=False, editable=False)
    application_date = models.DateField(auto_created=True)


class Notification(models.Model):
    CHANNEL = [
        ('sms', 'short message service'),
        ('email', 'Email'),
        ('call', 'Call')
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    channel = models.CharField(max_length=50, choices=CHANNEL, default='email')
    message = models.TextField(null=True, blank=True)
