from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=35)

    def __str__(self):
        return self.Name


class Subject(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=35)
    Subject = models.OneToOneField(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class Quiz(models.Model):
    Description = models.CharField(max_length=200)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    Date_of_publish = models.DateTimeField(auto_now_add=True, null=True)
    Starting_Time = models.DateTimeField(null=True)
    Ending_Time = models.DateTimeField(null=True)
    Attendance_required = models.IntegerField(default=75, null=True)

    def __str__(self):
        return str(self.Description)
        
    
class Question(models.Model):
    Question_Text = models.CharField(max_length=500)
    Option1 = models.CharField(max_length=100)
    Option2 = models.CharField(max_length=100)
    Option3 = models.CharField(max_length=100, blank=True)
    Option4 = models.CharField(max_length=100, blank=True)
    Answer = models.CharField(max_length=100)
    QuizID = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Question_Text)

class Attendance(models.Model):
    Name = models.ForeignKey(Student, on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    Present = models.IntegerField()
    Total_Attendance = models.IntegerField()

    def __str__(self):
        return str(self.Name) + " -- " + str(self.Subject)

class QuizScore(models.Model):
    Name = models.ForeignKey(Student, on_delete=models.CASCADE)
    Quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    Marks_Obtained = models.PositiveIntegerField()
    Max_Marks = models.PositiveIntegerField()

    def __str__(self):
        return str(self.Name) + " -- " + str(self.Quiz)
    