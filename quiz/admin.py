from django.contrib import admin
from quiz.models import Question, Quiz, Student, Subject, Teacher, Attendance, QuizScore

# Register your models here.
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Attendance)
admin.site.register(QuizScore)

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('Date_of_publish',)

admin.site.register(Quiz,RatingAdmin)
