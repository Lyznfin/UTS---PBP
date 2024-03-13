from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Course, CourseSection, UserCourse
from .forms import UserCourseForm
from django.contrib import messages

class Index(ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            total_seconds = course.duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            course.duration_hours = hours
            course.duration_minutes = minutes
        return context

class DetailCourse(DetailView):
    template_name = 'courses/course-detail.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            user_added_course = UserCourse.objects.filter(user=user, course=course).exists()
        else:
            user_added_course = False
        context['user_added_course'] = user_added_course
        return context

    @method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
    def post(self, request, slug):
        if request.user.is_authenticated:
            form = UserCourseForm(request.POST)
            if form.is_valid():
                try:
                    course = form.save(commit=False)
                    course_object = Course.objects.get(pk=request.POST.get('course-id'))
                    course.course = course_object
                    course.user = request.user
                    course.save()
                    messages.success(request, 'Course has been successfully added!')
                except:
                    messages.error(request, 'Course is failed to be added!')
            return redirect('course-detail', slug=slug)
        else:
            return redirect('/login', need_account=True)

@method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
class CourseSections(DetailView):
    template_name = 'courses/course-section.html'
    model = CourseSection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object().course
        user = self.request.user
        if user.is_authenticated:
            user_added_course = UserCourse.objects.filter(user=user, course=course).exists()
        else:
            user_added_course = False
        context['user_added_course'] = user_added_course
        return context
    
@method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
class UserCourses(ListView):
    template_name = 'courses/user-course.html'
    model = UserCourse
    context_object_name = 'usercourses'
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        usercourse = super().get_queryset()
        return usercourse.filter(user=self.request.user)