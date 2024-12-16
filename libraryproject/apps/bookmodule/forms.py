# apps/bookmodule/forms.py
from django import forms
from .models import Address, Book,Student,Student2

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'edition']

        title = forms.CharField(
        max_length=100,
        required=True,
        label="Title",
        widget= forms.TextInput( attrs= {
        'placeholder':'',
        'class':"mycssclass",
        'id':'jsID'
        })
        )
        price = forms.DecimalField(
        required=True,
        label="Price",
        initial=0
        )
        edition = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput())
        
class StudentForm(forms.ModelForm):
    address = forms.ModelChoiceField(
        empty_label=None,
        queryset=Address.objects.all(),
        required=True,
        label="Address",
        widget=forms.Select(attrs={
            'class': "mycssclass",
            'id': 'jsID2'
        })
    )

    class Meta:
        model = Student
        fields = ['name', 'age', 'address']  # Make sure all are lowercase strings

    name = forms.CharField(
        max_length=100,
        required=True,
        label="Name",  # Changed from "Title" to "Name" for clarity
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': "mycssclass",
            'id': 'jsID'
        })
    )
    age = forms.IntegerField(
        required=True,
        label="Age",
        initial=20
    )
    
class StudentForm2(forms.ModelForm):

    address = forms.ModelMultipleChoiceField(
    label="Addresses",
    queryset=Address.objects.all().order_by("city"),
    widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Student2
        fields = ['name', 'age', 'address']  # Make sure all are lowercase strings

    name = forms.CharField(
        max_length=100,
        required=True,
        label="Name",  # Changed from "Title" to "Name" for clarity
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': "mycssclass",
            'id': 'jsID'
        })
    )
    age = forms.IntegerField(
        required=True,
        label="Age",
        initial=20
    )
