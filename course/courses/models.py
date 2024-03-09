from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Instructor(models.Model):
    username = models.CharField(max_length = 25, unique = True)
    youtube = models.URLField(max_length = 100, unique = True)

class CourseCategory(models.Model):
    class Categories(models.TextChoices):
        PYTHON = 'PY', _('Python')
        RUST = 'RS', _('Rust')
        JAVA = 'JV', _('Java')
        JAVASCRIPT = 'JS', _('JavaScript')
        C_SHARP = 'CS', _('C#')
        C_PLUS_PLUS = 'CPP', _('C++')
        HTML_CSS = 'HTSS', _('HTML/CSS')
        REACT = 'REA', _('React')
        ANGULAR = 'ANG', _('Angular')
        VUE = 'VUE', _('Vue.js')
        PHP = 'PHP', _('PHP')
        SWIFT = 'SW', _('Swift')
        KOTLIN = 'KT', _('Kotlin')
        GO = 'GO', _('Go')
        RUBY = 'RB', _('Ruby')
        SQL = 'SQL', _('SQL')
        MACHINE_LEARNING = 'ML', _('Machine Learning')
        DATA_SCIENCE = 'DS', _('Data Science')
        DATA_STRUCTURE_ALGORITHM = 'DSA', _('Data Structure and Algorithm')
        ARTIFICIAL_INTELLIGENCE = 'AI', _('Artificial Intelligence')
        BLOCKCHAIN = 'BC', _('Blockchain')
        DEVOPS = 'DO', _('DevOps')
        CLOUD_COMPUTING = 'CC', _('Cloud Computing')
        BACKEND = 'BE', _('Backend Development')
        FRONTEND = 'FE', _('Frontend Development')
        GAME_DEVELOPMENT = 'GAME', _('Game Development')
        MOBILE_DEVELOPMENT = 'MOB', _('Mobile App Development')
        WEB_DEVELOPMENT = 'WEB', _('Web Development')
        UI_UX = 'UIUX', _('UI/UX Design')
        DATABASES = 'DB', _('Databases')
        SECURITY = 'SEC', _('Cyber Security')
    category = models.Choices(max_length = 4, choices = Categories.choices)

class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50, unique = True)
    description = models.TextField(max_length = 500)
    slug = models.SlugField(unique = True, db_index = True)
    categories = models.ManyToManyField(CourseCategory)

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("course-detail", kwargs={"slug": self.slug})

#ini bingung mau ditaro langsung ke table course atau dipisah
class CoursePaidType(models.Model):
    class PaidTypes(models.TextChoices):
        PAID = 'P', _('Paid')
        FREE = 'F', _('Free')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid_type = models.Choices(max_length=1, choices=PaidTypes.choices)

class CoursePrice(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
        #price boong boongan, wkwkwk
    price = models.DecimalField(validators=[MinValueValidator(0)])

class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    pointer = models.TextField() # -> embedded yt video

    def get_absolute_url(self):
        #slugnya pake pk ae lh
        return reverse("section-detail", kwargs={"pk": self.pk})
    
