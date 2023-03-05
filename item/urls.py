from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('', views.browseItems, name='browseItems'),
    path('new/', views.addItem, name='newItem'),
    path('myitems/', views.allMyItems, name='myItems'),
    path('<int:pk>/delete/', views.deleteItem, name='deleteItem'),
    path('<int:pk>/edit/', views.editItem, name='editItem'),
    ]
