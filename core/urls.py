from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import *

core_router = DefaultRouter()
core_router.register(r"user", UserViewSet)
core_router.register(r"jobs", JobViewSet)
core_router.register(r"payment", PaymentViewSet)
core_router.register(r"application", ApplicationViewSet)
url_patterns = core_router.urls

url_patterns += [
    path("token/request/", CustomObtainTokenPairView.as_view(), name="token_request"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


]
