from django import forms
from .models import Ticket, Review
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "text_area"}),
        }


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
