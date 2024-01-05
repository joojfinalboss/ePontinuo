from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='paginainicial'),
    path('login/', views.usuario_login, name='login'),
    path('signup/', views.usuario_cadastro, name='signup'),
    path('logout/', views.usuario_logout, name='logout'),
    path('main/', views.usuario_analista, name='main')
]