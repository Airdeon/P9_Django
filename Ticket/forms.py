from django import forms
from .models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "text_area"}),
        }


class UserFollowForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]
