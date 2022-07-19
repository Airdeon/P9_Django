from django.urls import path
from .views import SubscribeView, UnsubscribeRedirectView, SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("unsubscribe/<str:pk>/", UnsubscribeRedirectView.as_view(), name="unsubscribe"),
]
