from django.urls import path
from .views import Index, DetailCourse, CourseSections

urlpatterns = [
    path('', Index.as_view()),
    path('<slug:slug>', DetailCourse.as_view(), name='course-detail'),
    path('section/<int:pk>', CourseSections.as_view(), name='course-section')
]
