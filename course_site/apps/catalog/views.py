from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Author, Page, Profile
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, LoginAuthForm, RequestCourseForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout
from django.core.paginator import Paginator


def user_room(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.username == 'admin':
        user_list = User.objects.all()

        new_user_list = []
        for i in range(0, len(user_list)):
            if user_list[i].username != 'admin':
                user_struct = {
                    'user': user_list[i],
                    'progress': user_list[i].profile.progress
                }
                new_user_list.append(user_struct)

        context = {'user_list': new_user_list}
        return render(request, "users/admin_room.html", context=context)
    else:
        return render(request, "users/user_room.html")


def course_list_view(request):
    course_list = Course.objects.all()

    active = True
    new_course_list = []
    for i in range(0, len(course_list), 3):
        course_k = []
        for j in range(i, i + 3):
            if j >= len(course_list):
                break
            course_k.append(course_list[j])
        course_list_k = {
            'courses': course_k,
            'active': active
        }
        if active:
            active = False
        new_course_list.append(course_list_k)

    context = {'course_list': new_course_list}

    return render(request, 'catalog/course_list.html', context=context)


class CourseListView(generic.ListView):
    model = Course
    # /courses/?page=2 - для перехода


class CourseDetailView(generic.DetailView):
    model = Course


class PageDetailView(generic.DetailView):
    model = Page


class LoanedCoursesByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing courses on loan to current user."""
    model = Course
    template_name = 'catalog/course_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        # return Course.objects.filter(self.request.user in attendants.all()).filter(status__exact='o').order_by('due_back')
        return Course.objects.filter(attendants__exact=self.request.user)

    # borrower = self.request.user


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
    course_list = Course.objects.all()

    k = 0
    active = True
    new_course_list = []
    for i in range(0, len(course_list), 3):
        course_k = []
        for j in range(i, i + 3):
            if (j >= len(course_list)):
                break

            course_k.append(course_list[j])
        course_list_k = {
            'courses': course_k,
            'active': active
        }
        if active:
            active = False
        new_course_list.append(course_list_k)

    context = {'course_list': new_course_list}

    return render(request, 'index.html', context=context)


def index2(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_courses = Course.objects.all().count()
    # num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context

    context = {
        'num_courses': num_courses,
        # 'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
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


def participate_in_course(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')
    record = Course.objects.get(id=course_id)
    record.status = 'o'
    # record.borrower = request.user
    record.attendants.add(request.user)
    record.save()
    # return page_detail(request, course_id, 1)
    return HttpResponseRedirect('/course/' + str(course_id) + '/' + str(1))


def request_course(request):
    if not request.user.is_authenticated:
        return redirect('login')
    form = RequestCourseForm(request.POST)
    form.data = form.data.copy()
    form.data['summary'] = form.data['title']
    form.data['title'] = form.data['title'][0:10]
    if len(form.data['summary']) > 10:
        form.data['title'] += '...'

    form.data['added_by'] = request.user
    form.save()
    return HttpResponseRedirect('/')


def page_detail(request, pk, pn):
    cur_course = Course.objects.get(id=pk)

    try:
        page = get_object_or_404(cur_course.pages.all().filter(number=pn))
        context = {
            'page': page,
            'amount_of_pages': page.course.amount_of_pages(),
            'next_page': pn + 1,
            'prev_page': pn - 1
        }
        print(page.content)
        print(page.course)
        print(page.number)
        print(page.course.amount_of_pages())
        return render(request, 'catalog/page_detail.html', context=context)
    except Http404:
        if pn > 0:
            return page_detail(request, pk, pn - 1)
        else:
            return HttpResponseRedirect('/course/' + str(pk))


def finish_course(request, course_id):
    course = Course.objects.get(id=course_id)
    player, created = Profile.objects.get_or_create(user=request.user)

    # course.status = 'o'
    request.user.profile.progress += 1
    request.user.save()
    # record.borrower = request.user
    # course.attendants.add(request.user)
    # course.save()
    return HttpResponseRedirect('/courses/')


def my_course_list_view(request):
    course_list = Course.objects.filter(attendants__exact=request.user)

    active = True
    new_course_list = []
    for i in range(0, len(course_list), 3):
        course_k = []
        for j in range(i, i + 3):
            if j >= len(course_list):
                break
            course_k.append(course_list[j])
        course_list_k = {
            'courses': course_k,
            'active': active
        }
        if active:
            active = False
        new_course_list.append(course_list_k)

    context = {'course_list': new_course_list}

    return render(request, 'catalog/course_list.html', context=context)


def user_detail(request, pk):
    user = User.objects.all()[pk - 1]
    context = {
        'user': user
    }
    return render(request, 'catalog/user_detail.html', context=context)