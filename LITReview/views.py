from operator import itemgetter
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

        tickets = Ticket.objects.filter(Q(user=self.request.user) | Q(user__in=user))
        reviews = Review.objects.filter(Q(ticket__in=tickets) | Q(user__in=user) | Q(user=self.request.user))

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
