from django.shortcuts import render, get_object_or_404
from .models import Item
import random

#  Create your views here.


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)
    random_items = related.order_by('?')[:10]

    return render(request, 'item/detail.html', {'item': item, "related":random_items})
