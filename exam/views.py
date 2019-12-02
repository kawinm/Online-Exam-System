from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView

from exam.models import Exam, Question, Choice, Answer, Mark
from user.models import Student

from user.forms import LoginForm

def main(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        smail = Student.objects.filter(email_id__iexact=username, )
        year = smail.values('year')
    else:
        return redirect('user:login')

    for y in year:
        exam = Exam.objects.filter(year__year = y['year'], )

    return render(request, 'exam/main.html', {'username': username, 'exam':exam, 'student':smail})

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
            print(user_id, question_id_list[i-1], request.POST[str(i)], pk)
            answer = Answer(student_id=user_id, qs_id = question_id_list[i-1], choice_id= request.POST[str(i)], exam_id = pk)
            answer.save()
            i+=1
        
        return redirect('exam:calculate_mark', exam=pk, student= user_id)

    username = request.COOKIES['username']
    smail = Student.objects.filter(email_id__iexact=username, )

    exam_details = Exam.objects.filter(pk= pk, )

    questions_list = Question.objects.filter(exam__pk= pk, )
    question_set = {}

    print(exam_details)
    print(smail)
    for word in questions_list:
        question = Question.objects.get(question_text= word, )
        a = question.id
        answer_list = Choice.objects.filter(question__pk = a)
        question_set[word] = list(answer_list)
    return render(request, 'exam/exam.html', {'question_set':question_set, 'student': smail, 'exam_details':exam_details})

def calculate_mark(request, exam, student):
    answer = Answer.objects.filter(exam_id = exam, student_id = student )

    mark = 0
    for ans in answer:
        ques = Question.objects.filter(pk = ans.qs_id )
        for qs in ques:
            correct_choice = qs.correct_answer
            if correct_choice == ans.choice_id:
                mark += 4

    marks = Mark(student_id= student,  exam_id = exam, mark = mark)
    marks.save()
    return HttpResponse("You scored: " + str(mark))