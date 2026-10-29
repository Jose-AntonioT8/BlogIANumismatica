from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nueva/', views.create, name='create'),
    path('articulo/<slug:slug>/', views.detail, name='detail'),
]
