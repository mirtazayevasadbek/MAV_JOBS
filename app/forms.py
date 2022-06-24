from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.transaction import atomic
from django.forms import Form, CharField, EmailField
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.models import User
from app.token import account_activation_token
from djangoProject.settings import EMAIL_HOST_USER


class RegisterForm(Form):
    username = CharField(max_length=255)
    email = EmailField()
    password = CharField(max_length=255)

    def clean_username(self):
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already sing in ')
        return username

    def clean_email(self):
        email = self.data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already sing in ')
        return email

    @atomic
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email')
        )
        user.set_password(self.cleaned_data.get('password'))
        user.save()


class LoginForm(Form):
    username = CharField(max_length=255, required=False)
    email = EmailField()
    password = CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email is not found')
        return email

    def clean_password(self):
        email = self.data.get('email')
        password = self.data.get('password')

        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise ValidationError('This is not your password ')
            return password
        else:
            raise ValidationError('Password entered error')


class ForgotPasswordForm(Form):
    email = EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This email is not registered ')
        return email


def send_email(email, request, _type):
    user = User.objects.get(email=email)
    subject = ' MAV Jobs activate your account'
    current_site = get_current_site(request)
    message = render_to_string('app/activation-password.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
        'token': account_activation_token.make_token(user),
    })

    from_email = EMAIL_HOST_USER
    recipient_list = [email]

    result = send_mail(subject, message, from_email, recipient_list)
    print('Send to MAIL')
