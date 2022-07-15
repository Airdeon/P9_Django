from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, FormView, DeleteView, UpdateView
from .models import Review, Ticket
from .forms import TicketForm, ReviewForm, PostReviewForm
from django.urls import reverse_lazy
from django.db.models import Q
from operator import itemgetter


class PostView(LoginRequiredMixin, CreateView):
    """creation of ticket"""

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Créer"
        return context


class CritiqueView(LoginRequiredMixin, CreateView):
    """creation of review"""

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
        context["submit_text"] = "Créer"
        return context


class PostReviewView(LoginRequiredMixin, FormView):
    """creation of ticket and review in same time"""

    template_name = "Ticket/post_review.html"
    form_class = PostReviewForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.user = self.request.user
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
    """display of personal ticket and review"""

    template_name = "Ticket/mypost.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reviews = Review.objects.filter(user=self.request.user)
        review_id = []
        for review in reviews:
            review_id.append(review.id)
        tickets = Ticket.objects.filter(Q(user=self.request.user) | Q(id__in=review_id))
        tickets_list = []
        for ticket in tickets:
            reviewed_ticket = []
            for review in reviews:
                if review.ticket == ticket:
                    reviewed_ticket = [review, ticket, review.time_created]
                    break
                else:
                    reviewed_ticket = [0, ticket, ticket.time_created]
            if len(reviews) == 0:
                reviewed_ticket = [0, ticket, ticket.time_created]
            tickets_list.append(reviewed_ticket)
        for review in reviews:
            if review.user == self.request.user:
                reviewed_ticket = [review, review.ticket, review.time_created]
                if reviewed_ticket not in tickets_list:
                    tickets_list.append(reviewed_ticket)
        context["user"] = self.request.user
        context["tickets"] = sorted(tickets_list, key=itemgetter(2), reverse=True)

        return context


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """Update your ticket"""

    model = Ticket
    template_name = "Ticket/post.html"
    form_class = TicketForm
    success_url = reverse_lazy("myposts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = self.object
        context["submit_text"] = "Modifier"
        return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """Update your review"""

    template_name = "Ticket/critique.html"
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy("myposts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket"] = self.object.ticket
        context["submit_text"] = "Modifier"
        return context


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    """delete your ticket"""

    model = Ticket
    template_name = "Ticket/delete_ticket.html"
    context_object_name = "ticket"
    success_url = reverse_lazy("myposts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Supprimer"
        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """Delete your review"""

    model = Review
    template_name = "Ticket/delete_review.html"
    context_object_name = "review"
    success_url = reverse_lazy("myposts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Supprimer"
        return context
