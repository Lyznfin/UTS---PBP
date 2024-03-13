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

@method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
class CourseSections(DetailView):
    template_name = 'courses/course-section.html'
    model = CourseSection

@method_decorator(login_required(login_url='/login' + '?need_account=true'), name='dispatch')
class AddUserCourse(View):
    def post(self, request, slug):
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
            return redirect(reverse('course-detail', kwargs={'slug':slug}))
        return redirect(reverse('course-detail', kwargs={'slug':slug}))