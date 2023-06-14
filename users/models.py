from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_premium = models.BooleanField(
        _("premium status"),
        default=False,
        help_text=_("Только определенные премиум-пользователи могут просматривать премиум-фильмы"),
    )
    premium_expiration = models.DateTimeField(
        _("premium expiration"),
        blank=True,
        null=True,
        help_text=_("Дата и время окончания премиум-статуса пользователя"),
    )
    is_banned = models.BooleanField(default=False)
    active_movie = models.ManyToManyField("movies.Movie", blank=True)
