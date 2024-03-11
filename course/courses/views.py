from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Course, CourseSection

class Index(ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 3

class DetailCourse(DetailView):
    template_name = 'courses/course-detail.html'
    model = Course

#class CourseSections(DetailView, LoginRequiredMixin):
#    template_name = 'courses/course-section.html'
#    model = CourseSection

@method_decorator(login_required(login_url='/login'), name='dispatch')
class CourseSections(View):
    def post(self):
        pass
    
    #@method_decorator(login_required(login_url='/login'))
    def get(self, request, pk, slug):
        section = CourseSection.objects.get(pk=pk)
        return render(request, 'courses/course-section.html', {'object': section})