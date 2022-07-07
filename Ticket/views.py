from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, FormView, RedirectView
from .models import Review, Ticket
from .forms import TicketForm, ReviewForm, PostReviewForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from operator import itemgetter


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


class MyPostView(LoginRequiredMixin, TemplateView):
    template_name = "Ticket/mypost.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reviews = Review.objects.filter(user=self.request.user)
        review_id = []
        for review in reviews:
            review_id.append(review.id)
        tickets = Ticket.objects.filter(Q(user=self.request.user) | Q(id__in=review_id))
        print(tickets)

        tickets_list = []
        for ticket in tickets:
            reviewed_ticket = []
            for review in reviews:
                if review.ticket == ticket:
                    reviewed_ticket = [review, ticket, review.time_created]
                    break
                else:
                    reviewed_ticket = [0, ticket, ticket.time_created]
            tickets_list.append(reviewed_ticket)
        context["user"] = self.request.user
        context["tickets"] = sorted(tickets_list, key=itemgetter(2), reverse=True)

        return context
