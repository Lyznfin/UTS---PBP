from django import forms
from .models import UserCourse, CourseSection, Course

class UserCourseForm(forms.ModelForm):
    class Meta:
       model = UserCourse
       fields = []