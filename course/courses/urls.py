from django.urls import path
from .views import Index, DetailCourse, CourseSections, UserCourses, AddCourse, RemoveCourse

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('user', UserCourses.as_view(), name='user-courses'),
    path('<slug:slug>', DetailCourse.as_view(), name='course-detail'),
    path('<slug:slug>/add', AddCourse.as_view(), name='add-course'),
    path('<slug:slug>/remove', RemoveCourse.as_view(), name='delete-course'),
    path('<slug:slug>/section/<int:pk>', CourseSections.as_view(), name='course-section')
]