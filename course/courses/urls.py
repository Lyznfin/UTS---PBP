from django.urls import path
from .views import Index, DetailCourse, CourseSections, UserCourses

urlpatterns = [
    path('', Index.as_view()),
    path('user', UserCourses.as_view(), name='user-courses'),
    path('<slug:slug>', DetailCourse.as_view(), name='course-detail'),
    path('<slug:slug>/add', DetailCourse.as_view(), name='add-course'),
    path('<slug:slug>/section/<int:pk>', CourseSections.as_view(), name='course-section')
]