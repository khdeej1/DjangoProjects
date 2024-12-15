from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    price = models.FloatField(default = 0.0)
    edition = models.SmallIntegerField(default = 1)

class Address(models.Model):
    city = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField(max_length = 50)
    age = models.IntegerField(default = 1, max_length=2)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)



