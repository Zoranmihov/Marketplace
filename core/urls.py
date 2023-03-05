from django.urls import path
from django.contrib.auth import views as authViews
from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
        path('', views.index, name='index'),
        path('register/', views.register, name='register'),
        path('login/', authViews.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
        path('logout/', views.logout_user, name='logout')
        
]