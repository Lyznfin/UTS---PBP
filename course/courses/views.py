from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Course, CourseSection

class Index(ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'

class DetailCourse(DetailView):
    template_name = 'courses/course-detail.html'
    model = Course

class CourseSections(DetailView):
    template_name = 'courses/course-section.html'
    model = CourseSection