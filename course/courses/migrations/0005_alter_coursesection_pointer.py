# Generated by Django 5.0.3 on 2024-03-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesection',
            name='pointer',
            field=models.TextField(max_length=400),
        ),
    ]
