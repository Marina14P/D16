from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('ad/create/', views.create_ad, name='create_ad'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:ad_id>/respond/', views.respond_to_ad, name='respond_to_ad'),
    path('responses/', views.manage_responses, name='manage_responses'),
    path('responses/<int:response_id>/accept/', views.accept_response, name='accept_response'),
    path('responses/<int:response_id>/delete/', views.delete_response, name='delete_response'),
]
