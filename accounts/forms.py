from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import CharField, Form, PasswordInput
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from .models import CustomUser

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert"> {e}</div>' for e in self]))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "security_question")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'email', 'password1', 'password2', 'security_question']:
            self.fields[field_name].help_text = None
            self.fields[field_name].label = ''  # 🔹 Hide label text
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control',
                    'placeholder': field_name.capitalize().replace('1', '').replace('2', ' confirmation')
                 })

        self.fields['security_question'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'What is your favorite color?'
             })

class CustomUserLogInForm(UserCreationForm):
    class Meta:
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password']:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'}
            )

class ResetPasswordForm(Form):
    username = CharField(max_length=100)
    password = CharField(max_length=100, widget=PasswordInput())
    securityQuestion = CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = "New password"
        self.fields['securityQuestion'].label = "What\'s your favorite color?"
        for field_name in ['username', 'password', 'securityQuestion']:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        answer = cleaned_data.get("securityQuestion")

        if not CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username doesn't exist")

        user = CustomUser.objects.get(username=username)
        if answer != str(user.security_question):
            raise ValidationError("Incorrect answer to security question")