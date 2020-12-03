from django.forms import ModelForm
from quiz.models import Question, Quiz
from django import forms

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['QuizID']

class QuestionForm2(forms.Form):
    question = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class': 'form-control form-control-lg','placeholder' : "Add Question here"}))
    option1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg','placeholder' : "Add first option here (Mandatory)"}))
    option2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg','placeholder' : "Add second option here (Mandatory)"}))
    option3 = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg','placeholder' : "Add third option here (Optional)"}))
    option4 = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg','placeholder' : "Add fourth option here (Optional)"}))
    answer = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg','placeholder' : "Add answer here"}))

class QuizForm(forms.Form):
    description = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'label': "Description",'class': 'form-control form-control-lg','placeholder' : "Enter the name of the quiz (Mandatory)"}))
    closing_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-lg','placeholder':'YYYY-MM-DD hh:mm eg: 2020-01-01 10:00(in 24 hour format)'}))
    starting_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-lg','placeholder':'YYYY-MM-DD hh:mm eg: 2020-01-01 10:00(in 24 hour format)'}))
    #input_formats = ['%d/%m/%Y'],widget=forms.DateTimeInput(attrs={'class': 'form-control form-control-lg','type': 'datetime-local',"pattern":"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"})

class QuizModelForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['Description', 'Starting_Time', 'Ending_Time']