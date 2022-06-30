from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from Ticket.models import Ticket, Review
from Accounts.models import UserFollows
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
        context["reviews"] = Review.objects.filter(Q(ticket__in=context["tickets"]) | Q(user__in=user) | Q(user=self.request.user))
        context["user"] = self.request.user

        return context
