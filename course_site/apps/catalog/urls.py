from django.urls import path, include
from . import views
from django.conf.urls import url

from .views import user_room

"""
urlpatterns = [
    path('', views.index, name='index'),
]
"""

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list_view, name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.authors_list, name='authors'),
    path('author/<int:pk>/', views.author_detail, name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

#    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name="register"),
#    path('logout/', views.logout_view, name="logout"),

    path("user_room/", views.user_room, name="user_room"),
    path("accounts/", include("django.contrib.auth.urls")),

]
