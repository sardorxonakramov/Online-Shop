from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

User = get_user_model()

class Avtomat_input:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    'class':"text-danger form-control form-control-lg",
                }
            )


class UserRegisterForm(Avtomat_input,UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password1", "password2"]



class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Parol", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=False
    )
    password2 = forms.CharField(
        label="Parolni Tasdiqlash", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Parollar mos emas!")
            if len(password1) < 8:
                raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
