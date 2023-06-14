from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.last_login is not None and (timezone.now() - user.last_login) > timedelta(weeks=2):
                    user.is_banned = True
                    user.save()
                    raise forms.ValidationError(
                        format_html(
                            "Вы не логинились в течение двух недель. Вы были заблокированы "
                            "Пожалуйста <a href='block-reset/'>Напишите нам</a>."
                        )
                    )
            except User.DoesNotExist:
                pass

        return cleaned_data

    def confirm_login_allowed(self, user):
        if user.is_banned:
            raise forms.ValidationError(
                format_html(
                    "Вы заблокированы. Вы не логинились в течение двух недель. "
                    "Пожалуйста <a href='block-reset/'>Напишите нам</a>."
                    # '<button type="submit" class="btn btn-success"> Написать нам </button>'
                )
            )
        super().confirm_login_allowed(user)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

