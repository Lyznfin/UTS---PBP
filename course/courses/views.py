from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Course, CourseSection, UserCourse, CourseCategory
from .forms import UserCourseForm
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

class Index(ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        durations = self.request.GET.getlist('duration')

        if durations:
            queryset = queryset.filter(self.get_duration_filter(durations))
        
        return queryset

    def get_duration_filter(self, durations):
        duration_filters = []

        for duration in durations:
            if duration == '1':
                duration_filters.append(Q(duration__lt=timezone.timedelta(minutes=30)))
            elif duration == '2':
                duration_filters.append(Q(duration__range=(timezone.timedelta(minutes=30), timezone.timedelta(minutes=60))))
            elif duration == '3':
                duration_filters.append(Q(duration__range=(timezone.timedelta(hours=1), timezone.timedelta(hours=2))))
            elif duration == '4':
                duration_filters.append(Q(duration__range=(timezone.timedelta(hours=2), timezone.timedelta(hours=5))))
            elif duration == '5':
                duration_filters.append(Q(duration__range=(timezone.timedelta(hours=5), timezone.timedelta(hours=10))))
            elif duration == '6':
                duration_filters.append(Q(duration__gte=timezone.timedelta(hours=10)))
        
        q_objects = Q()
        for q_obj in duration_filters:
            q_objects |= q_obj
        
        return q_objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            total_seconds = course.duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            course.duration_hours = hours
            course.duration_minutes = minutes
        context['categories'] = self.get_all_category()
        context['selected_durations'] = self.request.GET.getlist('duration')
        return context
    
    def get_all_category(self):
        list_category = CourseCategory.objects.all()
        return list_category

class DetailCourse(View):
    template_name = 'courses/course-detail.html'

    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        user = request.user
        user_added_course = UserCourse.objects.filter(user=user, course=course).exists()
        return render(request, self.template_name, {'course': course, 'user_added_course': user_added_course})

class AddCourse(View):
    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, slug):
        user = request.user
        course_id = request.POST.get('course-id')

        if course_id:
            course = get_object_or_404(Course, pk=course_id)
            user_course, created = UserCourse.objects.get_or_create(user=user, course=course)
            user_course.save()
            if created:
                messages.success(request, 'Course has been successfully added!')
            else:
                messages.info(request, 'Course is already added!')
        else:
            messages.error(request, 'Invalid course ID!')
        return redirect('course-detail', slug=slug)

class RemoveCourse(View):
    @method_decorator(login_required(login_url='/login?need_account=true'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, slug):
        user = request.user
        course_id = request.POST.get('course-id')

        if course_id:
            course = get_object_or_404(Course, pk=course_id)
            user_course = get_object_or_404(UserCourse, user=user, course=course)
            user_course.delete()
            messages.success(request, 'Course has been successfully removed!')
        else:
            messages.error(request, 'Invalid course ID!')
        return redirect('course-detail', slug=slug)

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
    paginate_by = 5

    def get_queryset(self):
        usercourse = super().get_queryset()
        return usercourse.filter(user=self.request.user)