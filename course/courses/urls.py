from django.urls import path
from .views import Index, DetailCourse, CourseSections, AddUserCourse

urlpatterns = [
    path('', Index.as_view()),
    path('<slug:slug>', DetailCourse.as_view(), name='course-detail'),
    path('<slug:slug>/add', AddUserCourse.as_view(), name='add-course'),
    path('<slug:slug>/section/<int:pk>', CourseSections.as_view(), name='course-section')
]