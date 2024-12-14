from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name= "books.index"),
path('index2/<int:val1>/', views.index2),
path('listbooks/', views.listbooks, name= "books.listbooks"),
path('<int:bookId>', views.viewbook,name="viewbook")
]