from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import usersprofile


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        usersprofile.objects.create(user=instance)


@receiver(post_save, sender=User)
def edit_userprofile(sender, instance, created, **kwargs):
    instance.usersprofile.save()
