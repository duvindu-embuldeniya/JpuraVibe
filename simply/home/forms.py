from django import forms
from . models import Topic, Room, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description']



class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise ValidationError("This Email Is Already Taken!")
        return email



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']



class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_user = self.instance

        if User.objects.filter(email = email).exclude(pk = current_user.pk).exists():
            raise ValidationError("This Email Is Already Taken!")
        return email