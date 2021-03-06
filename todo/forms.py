from django.forms import ModelForm
from .models import Todo
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['task', 'desc', 'imp']

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

