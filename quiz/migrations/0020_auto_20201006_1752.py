# Generated by Django 3.0.3 on 2020-10-06 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_student_subject_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='Date_of_publish',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='Ending_Time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='quiz',
            name='Subject',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Subject'),
        ),
    ]
