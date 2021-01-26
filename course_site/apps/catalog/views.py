from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, LoginAuthForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    # /books/?page=2 - для перехода

class BookDetailView(generic.DetailView):
    model = Book

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

def authors_list(request):
    authors = Author.objects.all()
    context = {
        'author_list': authors
    }
    return render(request, 'catalog/author_list.html', context=context)

def author_detail(request, pk):
    author = Author.objects.all()[pk-1]
    context = {
        'author': author
    }
    return render(request, 'catalog/author_detail.html', context=context)

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применен по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors
    }
    return render(request, 'index.html', context=context)

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print(form)
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginAuthForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    else:
        form = LoginAuthForm()

    return render(request, 'registration/login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('index')
