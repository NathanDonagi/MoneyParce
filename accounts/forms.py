from django.contrib.auth.forms import UserCreationForm
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
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = None
            self.fields[field_name].label = ''  # 🔹 Hide label text
            self.fields[field_name].widget.attrs.update(
                {'class': 'form-control',
                    'placeholder': field_name.capitalize().replace('1', '').replace('2', ' confirmation')
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