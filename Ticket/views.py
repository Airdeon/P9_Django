from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, FormView, RedirectView
from .models import Ticket, UserFollows
from .forms import TicketForm, UserFollowForm
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


class CritiqueView(LoginRequiredMixin, TemplateView):
    template_name = "Ticket/critique.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follow = UserFollows.objects.filter(user=self.request.user)
        user = []
        for user_follow in follow:
            user.append(user_follow.followed_user)
        context["tickets"] = Ticket.objects.filter(Q(user=self.request.user) | Q(user__in=user))
        print(context)
        return context


class SubscribeView(LoginRequiredMixin, CreateView):
    template_name = "Ticket/subscribe.html"
    model = UserFollows
    form_class = UserFollowForm

    def get_form_kwargs(self):
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""

        kwargs = super(SubscribeView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("subscribe")

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followed_user"] = self.model.objects.filter(user=self.request.user)

        context["follow_me"] = self.model.objects.filter(followed_user=self.request.user)
        print(context)
        return context


class UnsubscribeRedirectView(LoginRequiredMixin, RedirectView):
    url = "/Ticket/subscribe/"

    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs.get("pk")
        UserFollows.objects.get(followed_user_id=id, user=self.request.user).delete()

        return super().get_redirect_url(*args, **kwargs)
