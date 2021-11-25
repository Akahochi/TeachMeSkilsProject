from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.db.models import Q


User = get_user_model()

class RegistrationForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat the password')




    class Meta:
        model = User

        fields = ['email', 'avatar']
        labels = {
            # 'username': 'Имя ПОЛЬЗОВАТЕЛЯ',if use username and password
            'email': 'email'
        }



    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(
                'Passwords must match'
            )
        return self.cleaned_data['password2']


    def clean(self):
        user = User.objects.filter(email=self.cleaned_data['email']).first()

        if user:
            raise ValidationError('A user with such credentials already exists')
        return super().clean()


"""
Сдесь логин по username and password
"""
#
# class LoginForm(forms.Form):
#     username = forms.CharField(label='Имя пользователя')
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#
#     def clean(self):
#         user = authenticate(
#             username=self.cleaned_data['username'],
#             password=self.cleaned_data['password']
#         )
#         if not user:
#             raise ValidationError('Введенные данные не верны')
#         return self.cleaned_data

"""
Сдесь логин по email and password
"""


class LoginForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        user = authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        if not user:
            raise ValidationError('The entered data is incorrect')
        return self.cleaned_data