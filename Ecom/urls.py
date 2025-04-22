"""
URL configuration for Newpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product, name='product'),
    path('login/', views.login_view, name='login'),
    path('callback/', views.callback_view, name='callback'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
   
    path('add-product/', views.add_product, name='add_product'),
]
