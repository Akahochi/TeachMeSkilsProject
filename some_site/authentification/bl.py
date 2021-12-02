from authentification.forms import RegistrationForm


def save_user(form: RegistrationForm):
    user = form.save(commit=False)
    user.set_password(form.cleaned_data['password2'])
    user.save()