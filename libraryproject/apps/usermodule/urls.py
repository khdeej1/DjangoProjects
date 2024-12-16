from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name= "users.index"),
path('register', views.registerUser, name='users.register'),
    path('login', views.loginUser, name='users.login'),
    path('logout', views.logoutUser, name='users.logout'),

]