from django.urls import path
from .views import Index, DetailCourse

urlpatterns = [
    path('', Index.as_view()),
    path('<slug:slug>', DetailCourse.as_view(), name='course-detail')
]
