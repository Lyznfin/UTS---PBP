from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

class Index(ListView):
    pass

class DetailCourse(DetailView):
    pass