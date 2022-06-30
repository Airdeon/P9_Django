from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserFollows
from .forms import UserFollowForm

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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