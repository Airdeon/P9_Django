from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from Ticket.models import Ticket, UserFollows
from django.db.models import Q


class Index(LoginRequiredMixin, TemplateView):
    template_name = "LITReview/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        follow = UserFollows.objects.filter(user=self.request.user)
        user = []
        for user_follow in follow:
            user.append(user_follow.followed_user)
        context["tickets"] = Ticket.objects.filter(Q(user=self.request.user) | Q(user__in=user))
        print(context)
        return context
