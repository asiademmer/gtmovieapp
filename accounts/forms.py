from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
import re

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Enter a ***valid*** email address."
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1',
        'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )

        self.fields['password1'].help_text = (
            "Your password must meet the following criteria:<br>"
            "✅ At least <strong>8 characters</strong> long<br>"
            "✅ Contain <strong>at least one uppercase letter</strong><br>"
            "✅ Contain <strong>at least one number</strong><br>"
            "❌ Cannot include <strong>&lt;, &gt;, !, @, or #</strong>"
        )

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        # Enforce minimum length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Enforce at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Enforce at least one digit
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")

        # Restrict certain characters (example: spaces and special symbols)
        if re.search(r'[<>!@#]', password):  # Add more restricted characters if needed
            raise ValidationError("Password cannot contain <, >, !, @, or #.")

        return password

class Meta:
    model = User
    fields = ("username", "email", "password1", "password2")

def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data["email"]
    if commit:
        user.save()
    return user