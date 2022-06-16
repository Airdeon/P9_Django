# Generated by Django 4.0.5 on 2022-06-16 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ticket', '0002_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollows',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
    ]
