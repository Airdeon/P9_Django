from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, FormView, RedirectView
from .models import Ticket, UserFollows
from .forms import TicketForm, UserFollowForm
from django.urls import reverse_lazy


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


class CritiqueView(LoginRequiredMixin, TemplateView):
    template_name = "Ticket/critique.html"


class SubscribeView(LoginRequiredMixin, CreateView):
    template_name = "Ticket/subscribe.html"
    model = UserFollows
    form_class = UserFollowForm

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
        id = self.kwarg.get("pk")

        return super().get_redirect_url(*args, **kwargs)
