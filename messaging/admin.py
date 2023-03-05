from django.contrib import admin

from .models import Messaging 
from .models import ConversationMessages

admin.site.register(Messaging)
admin.site.register(ConversationMessages)
