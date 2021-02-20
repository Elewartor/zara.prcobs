from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create/', views.create_reference_view, name='create_reference'),
    path('reference/<slug:slug>/', views.reference_view, name='reference_view'),
]