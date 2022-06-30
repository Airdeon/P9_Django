from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True, verbose_name="Description")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur", default=1)
    image = models.ImageField(upload_to="images", null=True, blank=True, verbose_name="Image")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Ticket")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(max_length=8192, blank=True, verbose_name="Commentaire")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
