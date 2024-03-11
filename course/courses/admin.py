from django.contrib import admin
from .models import Instructor, CourseCategory, Course, CoursePrice, CourseSection, UserCourse

# Register your models here.
admin.site.register(Instructor)
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CoursePrice)
admin.site.register(CourseSection)
admin.site.register(UserCourse)