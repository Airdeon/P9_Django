from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur", related_name="following", default=1)
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur", related_name="followed_by")

    class Meta:
        unique_together = ("user", "followed_user")

    def __str__(self):
        return self.user
