from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile


class LoginForm(AuthenticationForm):

    username = forms.CharField(max_length=100)
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ["username", "password"]:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            widget = self.fields[field_name].widget
            widget.attrs.update({
                "class": "form-control",
            })


class ProfileSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("bio", "image")

        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "style": "resize: none;",
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control",
            })
        }
