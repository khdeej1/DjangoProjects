from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name= "books.index"),
path('index2/<int:val1>/', views.index2),
path('listbooks/', views.listbooks, name= "books.listbooks"),
path('<int:bookId>', views.viewbook,name="viewbook"),
path('searchBook/', views.searchBook,name="searchBook"),
path('findBook/', views.findBook,name="books.findBook"),
path('simpleQuery/', views.simple_query,name="books.simpleQuery"),
path('complex_query/', views.complex_query,name="books.complex_query"),
path('task1/', views.task1,name="books.task1"),
path('task2/', views.task2,name="books.task2"),
path('task3/', views.task3,name="books.task3"),
path('task4/', views.task4,name="books.task4"),
path('task5/', views.task5,name="books.task5"),
path('task7/', views.showStudentsInCity,name="books.task7"),
]