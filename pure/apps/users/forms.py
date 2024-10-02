from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm

from apps.users.models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")
