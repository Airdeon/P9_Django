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

from django.urls import path
from .views import (
    PostView,
    CritiqueView,
    PostReviewView,
    MyPostView,
    TicketDeleteView,
    ReviewDeleteView,
    TicketUpdateView,
    ReviewUpdateView,
)

urlpatterns = [
    path("myposts/", MyPostView.as_view(), name="myposts"),
    # Ticket
    path("posts/", PostView.as_view(), name="posts"),
    path("update_ticket/<str:pk>/", TicketUpdateView.as_view(), name="update_ticket"),
    path("delete_ticket/<str:pk>/", TicketDeleteView.as_view(), name="delete_ticket"),
    # Review
    path("critique/<str:pk>/", CritiqueView.as_view(), name="critique"),
    path("update_review/<str:pk>/", ReviewUpdateView.as_view(), name="update_review"),
    path("delete_review/<str:pk>/", ReviewDeleteView.as_view(), name="delete_review"),
    # ticket and review
    path("post_review/", PostReviewView.as_view(), name="post_review"),
]
