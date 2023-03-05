from django import forms

from .models import ConversationMessages

class ConversationMessagesFrom(forms.ModelForm):
    class Meta:
        model = ConversationMessages
        fields = ('content',)