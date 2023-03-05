import os
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Item, Category
from .forms import NewItemForm, EditItemForm


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related = Item.objects.filter(
        category=item.category, is_sold=False).exclude(pk=pk)
    random_items = related.order_by('?')[:10]

    return render(request, 'item/detail.html', {'item': item, "related": random_items})


def browseItems(request):
    item_list = Paginator(Item.objects.filter(
        is_sold=False).order_by('created_at').reverse(), 15)
    page = request.GET.get('page')
    items = item_list.get_page(page)
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)
    query = request.GET.get('query', "")

    if category_id:
        item_list = Paginator(Item.objects.filter(is_sold=False).filter(
            category_id=category_id).order_by('created_at').reverse(), 15)
        items = item_list.get_page(page)

    if query:
        item_list = Paginator(Item.objects.filter(is_sold=False).filter(Q(name__icontains=query) |
                                                                        Q(description__icontains=query)).order_by('created_at').reverse(), 1)
        items = item_list.get_page(page)

    return render(request, 'item/browseItems.html', {"items": items, "query": query, "categories": categories, 'category_id': int(category_id)})


@login_required
def addItem(request):
    form = NewItemForm(request.POST, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    return render(request, 'item/form.html', {'form': form})


@login_required
def allMyItems(request):
    item_list = Paginator(Item.objects.filter(
        created_by=request.user).order_by('created_at').reverse(), 15)
    page = request.GET.get('page')
    items = item_list.get_page(page)

    return render(request, 'item/myItems.html', {'items': items})


@login_required
def deleteItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if len(item.image) > 0:
        os.remove(item.image.path)
    item.delete()
    return redirect('item:myItems')


@login_required
def editItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    form = EditItemForm(instance=item)
    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:myItems')

    return render(request, 'item/editForm.html', {'form': form})
