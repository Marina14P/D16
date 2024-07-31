"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('ad/create/', views.create_ad, name='create_ad'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:ad_id>/respond/', views.respond_to_ad, name='respond_to_ad'),
    path('responses/', views.manage_responses, name='manage_responses'),
    path('responses/<int:response_id>/accept/', views.accept_response, name='accept_response'),
    path('responses/<int:response_id>/delete/', views.delete_response, name='delete_response'),
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

