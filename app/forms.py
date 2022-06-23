from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import Form, CharField, EmailField

from app.models import User


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
            raise ValidationError('Kechirasiz hali bunday email yo`q ')
        return email

    def clean_password(self):
        email = self.data.get('email')
        password = self.data.get('password')

        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise ValidationError('Password yoki email xato terildi !')
            return password
        else:
            raise ValidationError('Password xato terildi !')
