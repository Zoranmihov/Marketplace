from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from item.models import Item
from .models import Messaging
from .forms import ConversationMessagesFrom

@login_required
def newConversation(request, itemPk):

    item = get_object_or_404(Item, pk=itemPk)

    if item.created_by == request.user:
        return redirect('core:index')
    
    conversations = Messaging.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('messaging:detail', conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessagesFrom(request.POST)
        if form.is_valid():
            conversation = Messaging.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation.message = form.save(commit=False)
            conversation.message.conversation = conversation
            conversation.message.created_by = request.user
            conversation.message.save()

            return redirect('item:detail', pk=itemPk)
        
    else:
        form = ConversationMessagesFrom()
        return render(request, 'messaging/new.html', {"form": form})

@login_required
def inbox(request):
    conversations = Messaging.objects.filter(members__in=[request.user.id])

    return render(request, 'messaging/inbox.html', {'conversations':conversations})

@login_required
def detail(request, pk):
    conversation = Messaging.objects.filter(members__in=[request.user.id]).get(pk=pk)
    if request.method == 'POST':
        form = ConversationMessagesFrom(request.POST)
        if form.is_valid():
            conversation.message = form.save(commit=False)
            conversation.message.conversation = conversation
            conversation.message.created_by = request.user
            conversation.message.save()
            conversation.save()

            return redirect('messaging:detail', pk=pk)
        
    form = ConversationMessagesFrom()
    return render(request, 'messaging/conversation.html', {'conversation':conversation, 'form':form})