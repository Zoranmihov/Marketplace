from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

from item.models import Category, Item
from .forms import SignUpForm

def index(request):
    item_list = Paginator(Item.objects.filter(is_sold = False).order_by('created_at').reverse(), 15)
    page = request.GET.get('page')
    items = item_list.get_page(page)
    categories = Category.objects.all()
    return render(request, 'core/index.html', {"categories": categories, "items": items})

def register(request):
    form = SignUpForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/login')
    return render(request, 'core/register.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('core:index')