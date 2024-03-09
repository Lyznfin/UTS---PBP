# Generated by Django 5.0.3 on 2024-03-09 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecategory',
            name='category',
            field=models.CharField(choices=[('PY', 'Python'), ('RS', 'Rust'), ('JV', 'Java'), ('JS', 'JavaScript'), ('CS', 'C#'), ('CPP', 'C++'), ('HTSS', 'HTML/CSS'), ('REA', 'React'), ('ANG', 'Angular'), ('VUE', 'Vue.js'), ('PHP', 'PHP'), ('SW', 'Swift'), ('KT', 'Kotlin'), ('GO', 'Go'), ('RB', 'Ruby'), ('SQL', 'SQL'), ('ML', 'Machine Learning'), ('DS', 'Data Science'), ('DSA', 'Data Structure and Algorithm'), ('AI', 'Artificial Intelligence'), ('BC', 'Blockchain'), ('DO', 'DevOps'), ('CC', 'Cloud Computing'), ('BE', 'Backend Development'), ('FE', 'Frontend Development'), ('GAME', 'Game Development'), ('MOB', 'Mobile App Development'), ('WEB', 'Web Development'), ('UIUX', 'UI/UX Design'), ('DB', 'Databases'), ('SEC', 'Cyber Security')], max_length=4, unique=True),
        ),
    ]
