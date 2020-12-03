"""CAA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz import views

urlpatterns = [
    #authentication
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    #admin
    path('admin/', admin.site.urls),

    #teacher
    path('teacher/', views.index, name="index"),

    path('quizlist/', views.quiz, name = "List"),
    path('<int:quiz_id>/questionlist/', views.queslist, name = "queslist"),

    path('createquiz/', views.createquiz, name = "createquiz"),
    path('createques/', views.createquestion, name = "createques"),
    
    path('deleteques/<int:id>', views.deleteques, name = "deleteques"),
    path('editques/<int:id>', views.editques, name = "editques"),
    path('updateques/<int:id>', views.updateques, name = "updateques"),
    path('addquestions/<int:id>', views.addques, name = "addques"),

    path('deletequiz/<int:id>', views.deletequiz, name = "deletequiz"),
    path('editquiz/<int:id>', views.editquiz, name = "editquiz"),
    path('updatequiz/<int:id>', views.updatequiz, name = "updatequiz"),

    path('viewattendance/', views.viewAttendance, name="viewAttendance"),
    path('markattendance/', views.markAttendance, name="markAttendance"),

    path('resultquizlist/', views.resultquizlist, name="resultquizlist"),
    path('<int:id>/result', views.result, name="result"),

    path('viewattendance/viewAttendanceData/', views.viewAttendanceData, name="attendancedata"),
    path('<int:id>/resultData/', views.resultData, name="resultData"),

    #student
    path('student/', views.studentindex, name = "studentindex"),

    path('myattendance/', views.myattendance, name="myAttendance"),

    path('subjectresult/', views.subjectresult, name="subjectresult"),
    path('<int:id>/myresult/', views.studentquizresult, name="myresult"),

    path('subjects/', views.subjectlist, name="subjects"),
    path('<int:id>/pendingquiz/', views.assignedquiz, name="assignedquiz"),
    path('<int:id>/attemptquiz', views.attemptQuiz, name="attemptquiz"),

    path('myattendance/myAttendanceData/', views.myAttendanceData, name="myattendancedata"),
    path('<int:id>/myresult/myresultdata/', views.studentquizresultdata, name="myresultdata"),

    #rough
    path('chart/', views.chart),

    #management
    path('management/', views.managementindex),

    path('studentslist/', views.studentList, name="studentlist"),
    path('teacherlist/', views.teacherList, name="teacherlist"),

    path('<int:id>/studentprogress/', views.studentProgress, name="studentprogress"),

    path('<int:id>/studentprogress/firstsubresult/', views.firstsubdata, name="firstsubdata"),
    path('<int:id>/studentprogress/secondsubresult/', views.secondsubdata, name="secondsubdata"),
    path('<int:id>/studentprogress/result/', views.jsondataresult, name="jsondataresult" ),

    path("<int:id>/teacherprogress/", views.teacherProgress, name="teacherprogress")
]
