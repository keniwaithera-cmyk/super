"""
URL configuration for supermarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


urlpatterns = [

    path('pos/', views.pos, name='pos'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('receipt/<int:transaction_id>/', views.receipt, name='receipt'),
    path('products/', views.products, name='products'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mylogin/', views.login, name='mylogin'),
    path('login/', views.login, name='login'),  # <--- added

]

