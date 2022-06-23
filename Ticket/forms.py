from django import forms
from .models import Ticket, Review, UserFollows
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "text_area"}),
        }


class UserFollowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserFollowForm, self).__init__(*args, **kwargs)
        queryset = User.objects.exclude(username=self.request.user.username)
        userfollow = UserFollows.objects.filter(user=self.request.user)
        print(userfollow)
        for user in userfollow:
            queryset = queryset.exclude(id=user.followed_user.id)
        self.fields["followed_user"].queryset = queryset

    class Meta:
        model = UserFollows
        fields = ["followed_user"]
