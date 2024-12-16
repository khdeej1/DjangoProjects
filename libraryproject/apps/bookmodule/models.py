from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length = 50)
    author = models.CharField(max_length = 50)
    price = models.FloatField(default = 0.0)
    edition = models.SmallIntegerField(default = 1)

class Address(models.Model):
    city = models.CharField(max_length=50)
    
    def __str__(self):
        return self.city

class Student(models.Model):
    name = models.CharField(max_length = 50)
    age = models.IntegerField(default = 1, max_length=2)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    
    
class Student2(models.Model):
    name = models.CharField(max_length = 50)
    age = models.IntegerField(default = 1, max_length=2)
    address = models.ManyToManyField(Address)





class StudentWithImage(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=20)
    profile_image = models.ImageField(upload_to='student_images/')

    def __str__(self):
        return self.name