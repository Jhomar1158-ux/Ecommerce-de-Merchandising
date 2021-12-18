from django.urls import path 
from app1 import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login', views.login_template),
    path('logout', views.logout),
    path('login_process', views.login_process),
    path('secret', views.secret),
    path('register', views.register_template),
    path('registro_process',views.registro_process),
    path('addToCard/<int:id>/', views.addToCard),
]
