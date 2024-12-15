from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, Min, Max, Sum, Avg,Count
from .models import Address, Book, Student

# Create your views here.
def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html" , {"name": name})    

def index2(request, val1 = 0):   #add the view function (index2)
    return HttpResponse("value1 = "+str(val1))



def viewbook(request, bookId):
    # assume that we have the following books somewhere (e.g. database)
    book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
    book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId: targetBook = book1
    if book2['id'] == bookId: targetBook = book2
    context = {'book':targetBook} # book is the variable name accessible by the template
    return render(request, 'bookmodule/show.html', context)
def listbooks(request):
    return render(request, 'bookmodule/listbooks.html')

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def searchBook(request):
    return render(request, 'bookmodule/search.html')

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def findBook(request):
    if request.method == "POST":
            string = request.POST.get('keyword').lower()
            isTitle = request.POST.get('option1')
            isAuthor = request.POST.get('option2')
            # now filter
            books = __getBooksList()
            newBooks = []
            for item in books:
                contained = False
                if isTitle and string in item['title'].lower(): contained = True
                if not contained and isAuthor and string in item['author'].lower():contained = True
                
                if contained: newBooks.append(item)
            return render(request, 'bookmodule/bookList.html', {'books':newBooks})
 
def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='of') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull = False).filter(title__icontains='of').filter(edition__gte = 2).exclude(price__lte = 100)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task1(request):
    bks = Book.objects.filter(Q(price__lte = 50))
    if len(bks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':bks})
    else:
        return render(request, 'bookmodule/index.html')

# books that have editions higher than two and either the title or author of the book contains the two adjacent letters ‘qu’ 
def task2(request):
    bks = Book.objects.filter(Q(edition__gt = 2) & (Q(title__icontains="qu") | Q(author__icontains="qu")))
    if len(bks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':bks})
    else:
        return render(request, 'bookmodule/index.html')

def task3(request):
    bks = Book.objects.filter(~Q(edition__gt = 2) & (~Q(title__icontains="qu") | ~Q(author__icontains="qu")))
    if len(bks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':bks})
    else:
        return render(request, 'bookmodule/index.html')


def task4(request):
    bks = Book.objects.all().order_by("title")
    return render(request, 'bookmodule/bookList.html', {'books':bks})

# number of books, total price of all books, average price, maximum price, and minimum price 
def task5(request):
   
    query = Book.objects.aggregate( numBooks = Count('title'),  totPrice = Sum('price' , default=0)
    ,avgPrice = Avg('price' , default=0)
    ,maxPrice = Max('price' , default=0)
    ,minPrice = Min('price' , default=0))

    return render(request, 'bookmodule/task5.html', {'statistics':query})


def showStudentsInCity(request):
    students_per_city = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/task7.html', {'data':students_per_city})

