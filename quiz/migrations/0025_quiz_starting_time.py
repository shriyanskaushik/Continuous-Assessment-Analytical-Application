# Generated by Django 3.0.3 on 2020-10-13 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0024_quiz_attendance_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='Starting_Time',
            field=models.DateTimeField(null=True),
        ),
    ]
