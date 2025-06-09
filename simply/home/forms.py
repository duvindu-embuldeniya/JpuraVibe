from django import forms
from . models import Topic, Room, Message

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = []