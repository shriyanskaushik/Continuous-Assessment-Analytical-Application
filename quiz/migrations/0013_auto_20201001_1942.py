# Generated by Django 3.0.3 on 2020-10-01 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_auto_20201001_1938'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
    ]
