from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q, Min, Max, Sum, Avg,Count
from .models import Address, Book, Student, Student2
from .forms import BookForm, StudentForm,StudentForm2, StudentWithImageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html" , {"name": name})    

def index2(request, val1 = 0):   #add the view function (index2)
    return HttpResponse("value1 = "+str(val1))



def viewbook(request, bookId):
    print(bookId)
    targetBook = Book.objects.get(id=bookId)
    # print_list(targetBook)
    # book is the variable name accessible by the template
    return render(request, 'bookmodule/show.html', {'book':targetBook})

def listbooks(request):
    bks = Book.objects.all()
    return render(request, 'bookmodule/listbooks.html',{'books':bks})


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

def addBook(request):
    if request.method=='POST':
        title=request.POST.get('title')
        price=request.POST.get('price')
        edition=request.POST.get('edition')
        author=request.POST.get('author')
        obj = Book(title=title, price = float(price),edition = edition, author = author)
        obj.save()
        return redirect('books.viewBook', bookId=obj.id)
    return render(request, "bookmodule/addBook.html")


def updateBook(request, book_id):
    obj = Book.objects.get(id=book_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        edition = request.POST.get('edition')
        author = request.POST.get('author')
        obj.title = title
        obj.price = float(price)
        obj.edition = int(edition)
        obj.author = author
        obj.save()
        # After updating, redirect to the book detail view
        return redirect('books.viewBook', bookId=book_id)
    # For GET, you might want to show a form template, not 'listBooks.html'
    return render(request, "bookmodule/updateBook.html", {'book': obj})


def deleteBook(request,book_id):
    obj = Book.objects.get(id = book_id)
    if request.method=="POST" :
        obj.delete()
        return redirect('books.listbooks')
    return render(request, "bookmodule/deleteBook.html",{'obj':obj})

def lab9_part2_listbooks(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab9_part2_listbooks.html', {'books': books})

def lab9_part2_addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab9_part2.listbooks')
    else:
        form = BookForm()
    return render(request, 'bookmodule/lab9_part2_addbook.html', {'form': form})

def lab9_part2_editbook(request, book_id):
    obj = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('lab9_part2.listbooks')
    else:
        form = BookForm(instance=obj)
    return render(request, 'bookmodule/lab9_part2_editbook.html', {'form': form, 'book': obj})

def lab9_part2_deletebook(request, book_id):
    obj = Book.objects.get(id=book_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('lab9_part2.listbooks')
    return render(request, 'bookmodule/lab9_part2_deletebook.html', {'book': obj})

@login_required(login_url='/users/login')
def listStudents(request):
    students = Student.objects.all()
    return render(request, 'bookmodule/students/listStudents.html', {'students': students})

def addStudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students.listStudents')
    else:
        form = StudentForm()
    return render(request, 'bookmodule/students/addStudent.html', {'form': form})

def editStudent(request, student_id):
    obj = Student.objects.get(id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('students.listStudents')
    else:
        form = StudentForm(instance=obj)
    return render(request, 'bookmodule/students/editStudent.html', {'form': form, 'student': obj})

def deleteStudent(request, student_id):
    obj = Student.objects.get(id=student_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('students.listStudents')
    return render(request, 'bookmodule/students/deleteStudent.html', {'student': obj})


def listStudents2(request):
    students = Student2.objects.all()
    return render(request, 'bookmodule/students2/listStudents.html', {'students': students})


def addStudent2(request):
    if request.method == 'POST':
        form = StudentForm2(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students2.listStudents')
    else:
        form = StudentForm2()
    return render(request, 'bookmodule/students2/addStudent.html', {'form': form})

def editStudent2(request, student_id):
    obj = Student2.objects.get(id=student_id)
    if request.method == 'POST':
        form = StudentForm2(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('students2.listStudents')
    else:
        form = StudentForm2(instance=obj)
    return render(request, 'bookmodule/students2/editStudent.html', {'form': form, 'student': obj})

def deleteStudent2(request, student_id):
    obj = Student2.objects.get(id=student_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('students2.listStudents')
    return render(request, 'bookmodule/students2/deleteStudent.html', {'student': obj})



def addStudentWithImage(request):
    if request.method == 'POST':
        form = StudentWithImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('students.listStudentsWithImage')
    else:
        form = StudentWithImageForm()
    return render(request, 'bookmodule/students_with_image/add_student.html', {'form': form})

def listStudentsWithImage(request):
    from .models import StudentWithImage
    students = StudentWithImage.objects.all()
    return render(request, 'bookmodule/students_with_image/list_students.html', {'students': students})
