from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, FormView, RedirectView
from .models import Review, Ticket
from .forms import TicketForm, ReviewForm, PostReviewForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User


# Create your views here.
class PostView(LoginRequiredMixin, CreateView):
    template_name = "Ticket/post.html"
    model = Ticket
    form_class = TicketForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("index")

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CritiqueView(LoginRequiredMixin, CreateView):
    template_name = "Ticket/critique.html"
    model = Review
    form_class = ReviewForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("index")

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.ticket = Ticket.objects.get(id=self.kwargs.get("pk"))
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = Ticket.objects.get(id=self.kwargs.get("pk"))
        return context


class PostReviewView(LoginRequiredMixin, FormView):
    template_name = "Ticket/post_review.html"
    form_class = PostReviewForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save()
        review = Review(
            ticket=Ticket.objects.latest("id"),
            rating=form.cleaned_data["rating"],
            user=self.request.user,
            headline=form.cleaned_data["headline"],
        )
        if "body" in form.cleaned_data:
            review.body = form.cleaned_data["body"]
        review.save()

        return super().form_valid(form)
