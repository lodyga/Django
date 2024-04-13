from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation

app_name = "conversation"

@login_required
def new_view(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect("dashboard:index-view")

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        pass # redirect to conversation

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect("item:detail-view", pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    context = {"form": form}
    return render(request, "conversation/conv_new.html", context)

@login_required
def inbox_view(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    context = {"conversations": conversations}
    return render(request, "conversation/conv_inbox.html", context)

@login_required
def detail_view(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    context = {
        "conversation": conversation}
        # "from": form}
    return render(request, "conversation/conv_detail.html", context)

