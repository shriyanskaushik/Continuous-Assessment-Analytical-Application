# Generated by Django 3.0.3 on 2020-10-01 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0004_auto_20201001_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question_Text', models.CharField(max_length=500)),
                ('Option1', models.CharField(default='Option1', max_length=100)),
                ('Option2', models.CharField(default='Option2', max_length=100)),
                ('Option3', models.CharField(blank=True, max_length=100)),
                ('Option4', models.CharField(blank=True, max_length=100)),
                ('Answer', models.CharField(default='Answer not added', max_length=100)),
                ('QuizID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
            ],
        ),
    ]
