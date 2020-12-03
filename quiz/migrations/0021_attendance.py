# Generated by Django 3.0.3 on 2020-10-10 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0020_auto_20201006_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Present', models.IntegerField()),
                ('Total_Attendance', models.IntegerField()),
                ('Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Student')),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Subject')),
            ],
        ),
    ]
