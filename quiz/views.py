from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

from quiz.forms import QuestionForm, QuestionForm2, QuizForm, QuizModelForm
from quiz.models import Question, Quiz, Teacher, Student, Subject, Attendance, QuizScore
from quiz.decorators import unauthenticated_user, allowed_users, teacher_only

# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, 'quiz/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
@teacher_only
def index(request):

    return render(request,'quiz/LandingPage.html')

@login_required(login_url=login)
@teacher_only
def quiz(request):
    sub = get_object_or_404(Teacher, user = request.user).Subject
    quiz_list = get_list_or_404(Quiz, Subject = sub)
    return render(request, 'quiz/quizlist.html', {'quiz_list' : quiz_list})

@login_required(login_url="login")
@teacher_only
def createquiz(request):
    #quiz = Quiz.objects.latest('QuizID'), {'quiz':quiz}
    #quiz_id = request.POST.get('quizid')
    sub = get_object_or_404(Teacher, user = request.user).Subject

    if request.method == "POST":
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz_text = form.cleaned_data['description']
            closingtime = form.cleaned_data['closing_time']
            startingtime = form.cleaned_data['starting_time']
            newquiz = Quiz(Description=quiz_text, Ending_Time=closingtime, Subject=sub, Starting_Time=startingtime)
            newquiz.save()
            return HttpResponseRedirect(reverse('createques'))
        else:
            print("Invalid form")
    else:
        print("Not post")
        form = QuizForm()

    return render(request, "quiz/createquiz.html", {'form': form})


#return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required(login_url="login")
@teacher_only
def createquestion(request):

    form = QuestionForm2()
    q = Quiz.objects.last()

    if request.method == "POST" and "addmore" in request.POST:
        form = QuestionForm2(request.POST)

        if form.is_valid():
            ques = form.cleaned_data['question']
            opt1 = form.cleaned_data['option1']
            opt2 = form.cleaned_data['option2']
            opt3 = form.cleaned_data['option3']
            opt4 = form.cleaned_data['option4']
            ans = form.cleaned_data['answer']

            newques = Question(Question_Text=ques, Option1=opt1, Option2=opt2, Option3=opt3, Option4=opt4, Answer=ans, QuizID=q)
            newques.save()

            return redirect('createques')

    elif request.method == "POST" and "finish" in request.POST:
        form = QuestionForm2(request.POST)

        if form.is_valid():
            ques = form.cleaned_data['question']
            opt1 = form.cleaned_data['option1']
            opt2 = form.cleaned_data['option2']
            opt3 = form.cleaned_data['option3']
            opt4 = form.cleaned_data['option4']
            ans = form.cleaned_data['answer']

            newques = Question(Question_Text=ques, Option1=opt1, Option2=opt2, Option3=opt3, Option4=opt4, Answer=ans, QuizID=q)
            newques.save()

            return redirect("List")

    return render(request, "quiz/createquestion.html", {'form' : form})

@login_required(login_url="login")
@teacher_only
def queslist(request, quiz_id):
    questionlist = get_list_or_404(Question, QuizID = quiz_id)
    quiz = questionlist[0]
    quiz1 = get_object_or_404(Quiz, Description = quiz.QuizID)

    return render(request, "quiz/queslist.html", {'questionlist' : questionlist, 'quiz' : quiz, 'quizid' : quiz1})

@login_required(login_url="login")
@teacher_only
def deleteques(request, id):
    ques = get_object_or_404(Question, id = id)
    desc = ques.QuizID
    ques.delete()
    quiz = get_object_or_404(Quiz, Description = desc)
    quizid = quiz.id
    return HttpResponseRedirect(reverse('queslist', args=(quizid,)))

@login_required(login_url="login")
@teacher_only
def editques(request, id):
    question = get_object_or_404(Question, id = id)
    return render(request, 'quiz/editques.html', {'question' : question})

@login_required(login_url="login")
@teacher_only
def updateques(request, id):
    question = get_object_or_404(Question, id = id)
    desc = question.QuizID
    quiz = get_object_or_404(Quiz, Description = desc)
    quizid = quiz.id

    if request.method == "GET":
        form = QuestionForm(instance = question)
        return HttpResponseRedirect(reverse('queslist', args=(quizid,)))
    
    else:
        form = QuestionForm(request.POST, instance = question)
        form.save()
        return HttpResponseRedirect(reverse('queslist', args=(quizid,)))

@login_required(login_url="login")
@teacher_only
def deletequiz(request, id):
    quiz = get_object_or_404(Quiz, id = id)
    questions = Question.objects.filter(QuizID=quiz)
    questions.delete()
    quiz.delete()
    return HttpResponseRedirect(reverse('List'))

@login_required(login_url="login")
@teacher_only
def editquiz(request, id):
    quiz = get_object_or_404(Quiz, id = id)
    form = QuizModelForm()
    return render(request, 'quiz/editquiz.html', {'form' : form, 'quiz' : quiz})

@login_required(login_url="login")
@teacher_only
def updatequiz(request, id):
    quiz = get_object_or_404(Quiz, id = id)

    if request.method == "GET":
        form = QuizModelForm(instance = quiz)
        return HttpResponseRedirect(reverse('List'))
    
    else:
        form = QuizModelForm(request.POST, instance = quiz)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return HttpResponseRedirect(reverse('List'))
        else:
            print("form is invalid")
            print(form.errors)
    
    return render(request, 'quiz/editquiz.html', {'form' : form, 'quiz' : quiz})

@login_required(login_url="login")
@teacher_only
def addques(request, id):

    form = QuestionForm2()
    q = get_object_or_404(Quiz, id = id)

    if request.method == "POST" and "addmore" in request.method:
        form = QuestionForm2(request.POST)

        if form.is_valid():
            ques = form.cleaned_data['question']
            opt1 = form.cleaned_data['option1']
            opt2 = form.cleaned_data['option2']
            opt3 = form.cleaned_data['option3']
            opt4 = form.cleaned_data['option4']
            ans = form.cleaned_data['answer']

            newques = Question(Question_Text=ques, Option1=opt1, Option2=opt2, Option3=opt3, Option4=opt4, Answer=ans, QuizID=q)
            newques.save()

            return HttpResponseRedirect(reverse('addques', args=(id,)))

    elif request.method == "POST" and "finish" in request.POST:
        form = QuestionForm2(request.POST)

        if form.is_valid():
            ques = form.cleaned_data['question']
            opt1 = form.cleaned_data['option1']
            opt2 = form.cleaned_data['option2']
            opt3 = form.cleaned_data['option3']
            opt4 = form.cleaned_data['option4']
            ans = form.cleaned_data['answer']

            newques = Question(Question_Text=ques, Option1=opt1, Option2=opt2, Option3=opt3, Option4=opt4, Answer=ans, QuizID=q)
            newques.save()

            return HttpResponseRedirect(reverse('queslist', args=(id,)))
            #return HttpResponse("You've created the quiz successfully!!")

    return render(request, "quiz/createquestion.html", {'form' : form}) 

@login_required(login_url="login")
@teacher_only
def viewAttendance(request):
    sub = get_object_or_404(Teacher, user = request.user).Subject
    att = get_list_or_404(Attendance, Subject=sub)
    return render(request, 'quiz/viewAttendance.html', {'attendance':att,'subject':sub})

@login_required(login_url="login")
@teacher_only
def viewAttendanceData(request):
    sub = get_object_or_404(Teacher, user = request.user).Subject
    att = get_list_or_404(Attendance, Subject=sub)
    attendancedata = []

    for i in att:
        attendancepercentage = float(i.Present/i.Total_Attendance) * 100
        attendancedata.append({str(i.Name):attendancepercentage})

    return JsonResponse(attendancedata, safe=False)

@login_required(login_url="login")
@teacher_only
def markAttendance(request):
    sub = get_object_or_404(Teacher, user = request.user).Subject
    att = get_list_or_404(Attendance, Subject=sub)
    student = Student.objects.filter()

    if request.method == "POST" and "submit" in request.POST:
        print("Form is valid")
        presentstudent = request.POST.getlist('checks[]')
        num = int(request.POST.get('lectureno'))
        for i in presentstudent:
            std = get_object_or_404(Student, Name=i)
            p = get_object_or_404(Attendance, Name=std, Subject=sub)
            p.Present += num
            p.save()
        
        for i in student:
            tt = get_object_or_404(Attendance, Name=i, Subject=sub)
            tt.Total_Attendance += num
            tt.save()
    
        return redirect("viewAttendance")
        
    else:
        print("form is invalid")
    return render(request, 'quiz/markAttendance.html', {'attendance':att,'subject':sub})

@login_required(login_url="login")
@teacher_only
def resultquizlist(request):
    sub = get_object_or_404(Teacher, user = request.user).Subject
    quiz_list = get_list_or_404(Quiz, Subject = sub)
    return render(request, 'quiz/resultquizlist.html', {'quiz_list' : quiz_list})

@login_required(login_url="login")
@teacher_only
def result(request, id):
    try:
        res = get_list_or_404(QuizScore, Quiz=id)
    except:
        messages.error(request, "No result for this Quiz")
    else:
        return render(request, 'quiz/result.html', {'result' : res,'quiz' : res[0]})
    
    return redirect("resultquizlist")

@login_required(login_url="login")
@teacher_only
def resultData(request, id):
    marks = []
    try:
        res = get_list_or_404(QuizScore, Quiz = id)
    except:
        pass
    else:
        for i in res:
            markspercentage = float(i.Marks_Obtained/i.Max_Marks) * 100
            marks.append({str(i.Name):markspercentage})
    return JsonResponse(marks, safe=False)

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def tempshow(request):
    quiz = get_object_or_404(Quiz, id = 4)
    question = get_list_or_404(Question, QuizID = quiz)
    actualanswers = [i.Answer for i in question]
    useranswers = []

    if request.method == "POST" and "submit" in request.POST:
        
        for q in question:
            response = request.POST.get(str(q.id))
            useranswers.append(response)
    
        correctanswers = [i for i, j in zip(actualanswers, useranswers) if i == j]
        print("Your score is " + str(len(correctanswers)) + "/" + str(len(useranswers)))

    return render(request, 'quiz/show.html', {'question' : question, 'quiz' : quiz})

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def myattendance(request):
    std = get_object_or_404(Student, user = request.user)
    att = get_list_or_404(Attendance, Name=std)
    return render(request, 'quiz/myattendance.html', {'attendance':att,'student' : std.Name})

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def myAttendanceData(request):
    std = get_object_or_404(Student, user = request.user)
    att = get_list_or_404(Attendance, Name=std)
    attendancedata = []

    for i in att:
        attendancepercentage = float(i.Present/i.Total_Attendance) * 100
        attendancedata.append({str(i.Subject):attendancepercentage})

    return JsonResponse(attendancedata, safe=False)
    

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def subjectlist(request):
    sub = get_list_or_404(Subject)
    return render(request, 'quiz/subjectlist.html', {'subjects' : sub})

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def assignedquiz(request, id):
    std = get_object_or_404(Student, user = request.user)
    assignedquiz =[]
    unattemptedquiz = []
    try:
        totalquiz = get_list_or_404(Quiz, Subject = id)
    except:
        messages.info(request, "No quiz created so far for this subject")

        return redirect("subjects")
    else:
        now = timezone.now()
        
        for i in totalquiz:
            try:
                attemptedquiz = get_object_or_404(QuizScore, Quiz = i, Name=std)
                print(attemptedquiz)
                print(attemptedquiz.Marks_Obtained)
            except:
                unattemptedquiz.append(i)
            else:
                pass
        if unattemptedquiz:
            for i in unattemptedquiz:
                if (i.Ending_Time and now < i.Ending_Time):
                    assignedquiz.append(i)
                elif (i.Ending_Time and now > i.Ending_Time):
                    ques = get_list_or_404(Question, QuizID=i)
                    question = [i.Question_Text for i in ques]
                    quizscore = QuizScore(Name=std, Quiz=i, Marks_Obtained=0, Max_Marks=len(question))
                    quizscore.save()
                else:
                    pass
            
            if assignedquiz:
                return render(request, 'quiz/assignedquiz.html', {'quiz' : assignedquiz})
            else:
                messages.info(request, "No quiz assigned")
        else:
            messages.info(request, "You've attempted all the quiz assigned to you")

    return redirect("subjects")

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def attemptQuiz(request, id):
    std = get_object_or_404(Student, user = request.user)
    quiz = get_object_or_404(Quiz, id = id)
    closingtime = quiz.Ending_Time
    startingtime = quiz.Starting_Time
    question = get_list_or_404(Question, QuizID = quiz)
    sub = quiz.Subject
    req_att = quiz.Attendance_required
    checkattendance = get_object_or_404(Attendance, Subject = sub, Name = std)
    attendancepercentage = float(checkattendance.Present/checkattendance.Total_Attendance) * 100
    actualanswers = [i.Answer for i in question]
    useranswers = []
    userquizopeningtime = timezone.now()

    if attendancepercentage >= req_att:

        if userquizopeningtime > startingtime:
            if request.method == "POST" and "submit" in request.POST:
                now = timezone.now()
                for q in question:
                    response = request.POST.get(str(q.id))
                    useranswers.append(response)

                if now <= closingtime:
                    correctanswers = [i for i, j in zip(actualanswers, useranswers) if i == j]
                    print("Your score is " + str(len(correctanswers)) + "/" + str(len(useranswers)))
                    generatescore = QuizScore(Name=std, Quiz=quiz, Marks_Obtained=len(correctanswers), Max_Marks=len(useranswers))
                    generatescore.save()
                    messages.info(request, "You've submitted the quiz successfully, go to result section to check your score")
                    return redirect("subjects")

                else:
                    messages.info(request, "Time is up!!")
                    return redirect("subjects")

        else:
            messages.info(request, "Quiz has not started yet")
            return redirect("subjects")
    
    else:
        text = "You cannot attempt " + str(quiz) + " because your attendance in " + str(sub) +  " subject is " + str(attendancepercentage) + "%" + " and required is " + str(req_att) + "%" + " for this quiz"
        messages.info(request, text)
        return redirect("subjects")

    return render(request, 'quiz/attemptQuiz.html', {'question' : question, 'quiz' : quiz})

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def subjectresult(request):
    sub = get_list_or_404(Subject)
    return render(request, 'quiz/subjectresult.html', {'subjects' : sub})

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def studentquizresult(request, id):
    std = get_object_or_404(Student, user = request.user)
    sub = get_object_or_404(Subject, id = id)
    result = []
    try:
        quiz = get_list_or_404(Quiz, Subject=sub)
    except:
        messages.info(request, "No quiz for this subject")
        return redirect("subjectresult")
    else:
        for i in quiz:
            try:
                res = get_object_or_404(QuizScore, Quiz=i, Name=std)
            except:
                pass
            else:
                result.append(res)
        if result:
            return render(request, 'quiz/studentquizresult.html', {'result' : result,'sub': sub})
        else:
            text = "Your record is not updated, to update record go to quiz section and check for quiz"
            messages.info(request, text)
            return redirect("subjectresult")

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def studentquizresultdata(request, id):
    std = get_object_or_404(Student, user = request.user)
    sub = get_object_or_404(Subject, id = id)
    result = []
    jsondata = []
    try:
        quiz = get_list_or_404(Quiz, Subject=sub)
    except:
        messages.info(request, "No quiz for this subject")
        return redirect("subjectresult")
    else:
        for i in quiz:
            try:
                res = get_object_or_404(QuizScore, Quiz=i, Name=std)
            except:
                pass
            else:
                result.append(res)
        
        if result:
            for i in result:
                resultpercentage = float(i.Marks_Obtained/i.Max_Marks) * 100
                jsondata.append({str(i.Quiz):resultpercentage})

    return JsonResponse(jsondata, safe=False)

@login_required(login_url="login")
@allowed_users(allowed_roles=['student'])
def studentindex(request):

    return render(request,'quiz/StudentLandingPage.html')

def chart(request):
    return render(request, 'quiz/chart.html')

def managementindex(request):
    return render(request, 'quiz/managementLandingPage.html')

def studentList(request):
    std = get_list_or_404(Student)
    return render(request, 'quiz/studentList.html', {'student': std})

def teacherList(request):
    tch = get_list_or_404(Teacher)
    return render(request, 'quiz/teacherList.html', {'teacher': tch})

def studentProgress(request, id):
    std = get_object_or_404(Student, id = id)
    sub = get_list_or_404(Subject)
    firstsubquizscorelist = []
    secondsubquizscorelist = []
    thirdsubquizscorelist = []
    try:
        firstsubquiz = get_list_or_404(Quiz, Subject = sub[0])
        secondsubquiz = get_list_or_404(Quiz, Subject = sub[1])
        thirdsubquiz = get_list_or_404(Quiz, Subject = sub[2])
        sub1 = sub[0]
        sub2 = sub[1]
        sub3 = sub[2]
    except:
        pass
    else:
        if firstsubquiz:
            try:
                for i in firstsubquiz:
                    firstsubquizscore = get_object_or_404(QuizScore, Quiz = i, Name = std)
                    firstsubquizscorelist.append(firstsubquizscore)
            except:
                pass
                print("ERROR")
        if secondsubquiz:
            try:
                for i in secondsubquiz:
                    secondsubquizscore = get_object_or_404(QuizScore, Quiz = i, Name = std)
                    secondsubquizscorelist.append(secondsubquizscore)
            except:
                pass
        if thirdsubquiz:
            try:
                for i in thirdsubquiz:
                    thirdsubquizscore = get_object_or_404(QuizScore, Quiz = i, Name = std)
                    thirdsubquizscorelist.append(thirdsubquizscore)
            except:
                pass
    
    data = {'student': std, 'sub1': sub1, 'sub2': sub2, 'sub3': sub3, 'firstsubquizscore': firstsubquizscorelist, 'secondsubquizscore': secondsubquizscorelist, 'thirdsubquizscore': thirdsubquizscorelist, 'sec': secondsubquizscorelist}
    return render(request, 'quiz/studentProgress.html', data)

def firstsubdata(request, id):
    std = get_object_or_404(Student, id = id)
    sub = get_list_or_404(Subject)
    result = []
    jsondata = []
    try:
        firstsubquiz = get_list_or_404(Quiz, Subject = sub[0])
        
    except:
        pass
    else:
        for i in firstsubquiz:
            try:
                res = get_object_or_404(QuizScore, Quiz = i, Name = std)
            except:
                pass
            else:
                result.append(res)
        
        if result:
            for i in result:
                resultpercentage = float(i.Marks_Obtained/i.Max_Marks) * 100
                jsondata.append({str(i.Quiz):resultpercentage})

    return JsonResponse(jsondata, safe = False)

def secondsubdata(request, id):
    std = get_object_or_404(Student, id = id)
    sub = get_list_or_404(Subject)[1]
    result = []
    jsondata = []
    try:
        secondsubquiz = get_list_or_404(Quiz, Subject = sub)
    except:
        pass
    else:
        for i in secondsubquiz:
            try:
                res = get_object_or_404(QuizScore, Quiz = i, Name = std)
            except:
                pass
            else:
                result.append(res)
        
        if result:
            for i in result:
                resultpercentage = float(i.Marks_Obtained/i.Max_Marks) * 100
                jsondata.append({str(i.Quiz):resultpercentage})

    return JsonResponse(jsondata, safe = False)

def jsondataresult(request, id):
    std = get_object_or_404(Student, id = id)
    sub = get_list_or_404(Subject)
    firstsubquizscorelist = []
    firstsubquizscorelistresult = []
    secondsubquizscorelist = []
    secondsubquizscorelistresult = []
    thirdsubquizscorelist = []
    thirdsubquizscorelistresult = []
    try:
        firstsubquiz = get_list_or_404(Quiz, Subject = sub[0])
        secondsubquiz = get_list_or_404(Quiz, Subject = sub[1])
        thirdsubquiz = get_list_or_404(Quiz, Subject = sub[2])
    except:
        pass
    else:
        if firstsubquiz:
            
            try:
                
                for i in firstsubquiz:
                    firstsubquizscore = get_object_or_404(QuizScore, Quiz = i, Name = std)
                    firstsubquizscorelist.append(firstsubquizscore)
                
            except:
                pass
            finally:
                if firstsubquizscorelist:
                    for i in firstsubquizscorelist:
                        resultpercentage = float(i.Marks_Obtained/i.Max_Marks) * 100
                        firstsubquizscorelistresult.append({str(i.Quiz):resultpercentage})
                    
        if secondsubquiz:
            try:
                for i in secondsubquiz:
                    secondsubquizscore = get_object_or_404(QuizScore, Quiz = i, Name = std)
                    secondsubquizscorelist.append(secondsubquizscore)
            except:
                pass
            finally:
                if secondsubquizscorelist:
                    for i in secondsubquizscorelist:
                        resultpercentage = float(i.Marks_Obtained/i.Max_Marks) * 100
                        secondsubquizscorelistresult.append({str(i.Quiz):resultpercentage})
        if thirdsubquiz:
            try:
                for i in thirdsubquiz:
                    thirdsubquizscore = get_object_or_404(QuizScore, Quiz = i, Name = std)
                    thirdsubquizscorelist.append(thirdsubquizscore)
            except:
                pass
            finally:
                if thirdsubquizscorelist:
                    for i in thirdsubquizscorelist:
                        resultpercentage = float(i.Marks_Obtained/i.Max_Marks) * 100
                        thirdsubquizscorelistresult.append({str(i.Quiz):resultpercentage})
    data = {'firstsubquizscore': firstsubquizscorelistresult, 'secondsubquizscore': secondsubquizscorelistresult, 'thirdsubquizscore': thirdsubquizscorelistresult}
    return JsonResponse(data, safe = False)

def teacherProgress(request, id):
    tch = get_object_or_404(Teacher, id = id)
    sub = tch.Subject
    quizscorelist = []
    try:
        quiz = get_list_or_404(Quiz, Subject=sub)
    except:
        pass
    finally:
        if quiz:
            for i in quiz:
                quizscore = get_list_or_404(QuizScore, Quiz=i)
                quizscorelist.append(quizscore)
            print(quizscorelist)
            print(len(quizscorelist))
    return redirect("teacherlist")
