from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Agregar el campo email único
    USERNAME_FIELD = 'email'  # Usa el correo como el campo para iniciar sesión
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=150, blank=True, null=True)
