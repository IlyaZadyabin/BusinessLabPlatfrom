from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Book, Author, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, LoginAuthForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.paginator import Paginator


def user_room(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "users/user_room.html")


def book_list_view(request):
    book_list = Book.objects.all()

    k = 0
    active = True
    new_book_list = []
    for i in range(0, len(book_list), 3):
        book_k = []
        for j in range(i, i + 3):
            if (j >= len(book_list)):
                break

            book_k.append(book_list[j])
        book_list_k = {
            'books': book_k,
            'active': active
        }
        if active:
            active = False
        new_book_list.append(book_list_k)

    context = {'book_list': new_book_list}

    return render(request, 'catalog/book_list.html', context=context)


class BookListView(generic.ListView):
    model = Book
    # /books/?page=2 - для перехода


class BookDetailView(generic.DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Book
    template_name = 'catalog/book_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


def authors_list(request):
    authors = Author.objects.all()
    context = {
        'author_list': authors
    }
    return render(request, 'catalog/author_list.html', context=context)


def author_detail(request, pk):
    author = Author.objects.all()[pk - 1]
    context = {
        'author': author
    }
    return render(request, 'catalog/author_detail.html', context=context)


def index(request):
    book_list = Book.objects.all()

    k = 0
    active = True
    new_book_list = []
    for i in range(0, len(book_list), 3):
        book_k = []
        for j in range(i, i + 3):
            if (j >= len(book_list)):
                break

            book_k.append(book_list[j])
        book_list_k = {
            'books': book_k,
            'active': active
        }
        if active:
            active = False
        new_book_list.append(book_list_k)

    context = {'book_list': new_book_list}

    return render(request, 'index.html', context=context)


def index2(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
  # num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
   # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    context = {
        'num_books': num_books,
        #'num_instances': num_instances,
        #'num_instances_available': num_instances_available,
        'num_authors': num_authors
    }
    return render(request, 'index.html', context=context)


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # print(form)
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
            return redirect('user_room')
    else:
        form = LoginAuthForm()
    return render(request, 'registration/login.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect('index')


def update_variable(value):
    data = value
    return data


def add_loan(request, book_id):  # function is state of developing
    record = Book.objects.get(id=book_id)
    record.status = 'o'
    record.borrower = request.user
    record.save()
    return HttpResponseRedirect('/book/' + str(book_id))
