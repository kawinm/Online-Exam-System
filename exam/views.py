from django.shortcuts import render
from django.views.generic import ListView

from exam.models import Exam, Question, Choice
from user.models import Student

def main(request):
    username = request.COOKIES['username']

    smail = Student.objects.filter(email_id__iexact=username, )
    year = smail.values('year')

    for y in year:
        exam = Exam.objects.filter(year__year = y['year'], )

    return render(request, 'exam/main.html', {'username': username, 'exam':exam,})

def take_exam(request, pk):
    if request.method == "POST":
        username = request.COOKIES['username']

        smail = Student.objects.get(email_id__iexact=username, )
        user_id = smail.id

        question_id_list = []
        questions_list = Question.objects.filter(exam__pk= pk, )

        for word in questions_list:
            question = Question.objects.get(question_text= word, )
            a = question.id
            question_id_list.append(a)

        i = 1
        while i <= len(question_id_list):
            print(user_id, question_id_list[i-1], request.POST[str(i)])
            i+=1
        
        return render(request, 'exam/main.html',)
    questions_list = Question.objects.filter(exam__pk= pk, )
    context = {}

    for word in questions_list:
        question = Question.objects.get(question_text= word, )
        a = question.id
        answer_list = Choice.objects.filter(question__pk = a)
        context[word] = list(answer_list)
    return render(request, 'exam/exam.html', {'abc':context})