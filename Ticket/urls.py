"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import PostView, SubscribeView, CritiqueView, UnsubscribeRedirectView

urlpatterns = [
    path("posts/", PostView.as_view(), name="posts"),
    path("critique/", CritiqueView.as_view(), name="critique"),
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("unsubscribe/<str:pk>/", UnsubscribeRedirectView.as_view(), name="unsubscribe"),
]
