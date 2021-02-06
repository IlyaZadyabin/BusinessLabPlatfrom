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
    path('courses/', views.course_list_view, name='courses'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/<int:pk>/<int:pn>', views.page_detail, name='page_num'),
    path('authors/', views.authors_list, name='authors'),
    path('author/<int:pk>/', views.author_detail, name='author-detail'),
    path('user/<int:pk>/', views.user_detail, name='user-detail'),
    # path('mycourses/', views.LoanedCoursesByUserListView.as_view(), name='my_courses'),
    path('mycourses/', views.my_course_list_view, name='my_courses'),


    path('participate_in_course/<int:course_id>', views.participate_in_course, name='participate_in_course'),
    path('finish_course/<int:course_id>', views.finish_course, name='finish_course'),

    path('request_course/', views.request_course, name='request_course'),


#    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name="register"),
    path('accounts/logout/', views.logout_view, name="logout"),

    path("user_room/", views.user_room, name="user_room"),
    path("accounts/", include("django.contrib.auth.urls")),

]
