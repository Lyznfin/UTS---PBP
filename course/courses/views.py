from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Course, CourseSection, UserCourse, CourseCategory
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages

class Index(ListView):
    template_name = 'courses/index.html'
    model = Course
    context_object_name = 'courses'
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        duration_filter = self.request.GET.getlist('duration')

        if duration_filter:
            q_objects = Q()
            for duration in duration_filter:
                if duration == '1':
                    q_objects |= Q(duration__lt='00:30:00')
                elif duration == '2':
                    q_objects |= Q(duration__range=('00:30:00', '01:00:00'))
                elif duration == '3':
                    q_objects |= Q(duration__range=('01:00:00', '02:00:00'))
                elif duration == '4':
                    q_objects |= Q(duration__range=('02:00:00', '05:00:00'))
                elif duration == '5':
                    q_objects |= Q(duration__range=('05:00:00', '10:00:00'))
                elif duration == '6':
                    q_objects |= Q(duration__gte='10:00:00')
                    
            queryset = queryset.filter(q_objects)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for course in context['courses']:
            total_seconds = course.duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            course.duration_hours = hours
            course.duration_minutes = minutes
        context['categories'] = self.get_all_category()
        return context
    
    def get_all_category(self):
        list_category = CourseCategory.objects.all()
        return list_category
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return JsonResponse({'html': render_to_string('courses/course_list.html', context, request=self.request)})
        return super().render_to_response(context, **response_kwargs)

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