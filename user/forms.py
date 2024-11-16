from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")

    def clean_username(self):
        email = self.cleaned_data["username"]
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Correo electrónico no registrado")
        return email
