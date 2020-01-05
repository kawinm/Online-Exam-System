from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView

from exam.models import Exam, Question, Choice, Answer, Mark
from user.models import Student

from user.forms import LoginForm

from math import ceil

#Headers to generate pdf ReportLab
from django.http import FileResponse
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from textwrap import wrap

def main(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        smail = Student.objects.filter(email_id__iexact=username, )
        year = smail.values('year')
    else:
        return redirect('user:login')

    #for y in year:
        #exam = Exam.objects.filter(year__year = y['year'], )

    exam = Exam.objects.all()
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
            #print(user_id, question_id_list[i-1], request.POST[str(i)], pk)
            answer = Answer(student_id=user_id, qs_id = question_id_list[i-1], choice_id= request.POST[str(i)], exam_id = pk)
            answer.save()
            i+=1
        
        return redirect('exam:calculate_mark', exam=pk, student= user_id)

    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        smail = Student.objects.filter(email_id__iexact=username, )

        exam_details = Exam.objects.filter(pk= pk )

        questions_id_list = Question.objects.filter(exam__pk= pk ).values_list('id', flat=True)
        question_set = {}

        for word in questions_id_list:
            question = Question.objects.filter(pk= word ).values_list('question_text', flat=True)[0]
            answer_list = Choice.objects.filter(question__pk = word)
            question_set[question] = list(answer_list)
        return render(request, 'exam/exam.html', {'question_set':question_set, 'student': smail, 'exam_details':exam_details})
    else:
        return redirect('user:login')

def calculate_mark(request, exam, student):
    answer = Answer.objects.filter(exam_id = exam, student_id = student )
    exam_object = Exam.objects.filter(pk = exam)
    mark = 0
    for ans in answer:
        ques = Question.objects.filter(pk = ans.qs_id )
        for qs in ques:
            correct_choice = qs.correct_answer
            if correct_choice == ans.choice_id:
                mark += 4

    marks = Mark(student_id= student,  exam_id = exam, mark = mark)
    marks.save()

    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        smail = Student.objects.filter(email_id__iexact=username, )
        year = smail.values('year')
    else:
        return redirect('user:login')

    return render(request, 'exam/mark.html', {'username': username, 'exam':exam_object, 'student':smail, 'mark':mark})

def add_questions(request):
    if request.method == "POST":
        exam_name = request.POST.get('exam', "")
        qs_list = request.POST.get('qs', "")
        exam = Exam.objects.values_list('exam_name', flat=True)
        if exam_name not in exam:
            exam = Exam.objects.all()
            return render(request, 'exam/questions.html', {'exam':exam})
        
        exam_object = Exam.objects.get(exam_name= exam_name, )
        i = 0
        for text in qs_list.split("\n"):
            if i == 0:
                qs_text = str.strip(text)
                i = 1
                continue
            if i == 1:
                crct_ans = int(text)
                i = 2
                qs_object = Question.objects.create(exam= exam_object, question_text= qs_text, correct_answer = crct_ans)
                continue
            if len(text.strip()) == 0:
                i = 0
                continue
            choice_text = str.strip(text)
            choice_object = Choice.objects.create(question= qs_object, choice_text = choice_text)
        
        return redirect('admin:index')

    exam = Exam.objects.all()
    return render(request, 'exam/questions.html', {'exam':exam})

def generate_pdf(request, exam):
    exam_details = Exam.objects.filter(pk= exam )
    question_list = Question.objects.filter(exam__pk= exam, )
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)

    p.setFont('Helvetica', 36)
    for word in exam_details.values('exam_name'):
        exam_name = word['exam_name']
        p.drawString(75, 750, exam_name)
    x = 75
    y = 750
    i = 1
    page_number = 1
    PAGE_BREAK_COORDINATE = 150
    HORIZONTAL_WORD_LIMIT = 55

    for word in question_list.values('question_text'):
        if y < PAGE_BREAK_COORDINATE:
            p.setFont('Helvetica', 15)
            p.drawString(300, 40, str(page_number))
            page_number+=1
            p.showPage()
            y = 820
        p.setFont('Helvetica', 16)
        y -= 40
        t = p.beginText()
        t.setTextOrigin(x,y)
        qs_text = str(i) + ") "+ word['question_text']
        wraped_text = "\n".join(wrap(qs_text, HORIZONTAL_WORD_LIMIT))
        t.textLines(wraped_text)
        n = int(ceil(len(qs_text) / HORIZONTAL_WORD_LIMIT))
        p.drawText(t)
        i+= 1

        question = Question.objects.get(question_text= word['question_text'], )
        a = question.id
        choice_list = Choice.objects.filter(question__pk = a)
        y-= (15*n)
        j = 1
        for choice in choice_list.values('choice_text'):
            p.setFont('Helvetica', 14)
            y-= 25
            p.drawString(x, y, "     " + str(j) + ") "+ choice['choice_text'])
            j += 1
    if y >= PAGE_BREAK_COORDINATE:
        p.setFont('Helvetica', 15)
        p.drawString(300, 40, str(page_number))
            

    # Close the PDF object cleanly, and we're done.
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=exam_name+'.pdf')

def review_exam(request, exam, student):

    answer = Answer.objects.filter(exam_id=exam, student_id=student )
    correct_answer = []
    for ans in answer:
        ques = Question.objects.filter(pk = ans.qs_id )
        for qs in ques:
            correct_choice = qs.correct_answer
            correct_answer.append(correct_choice)
            

    username = request.COOKIES['username']
    smail = Student.objects.filter(email_id__iexact=username, )

    exam_details = Exam.objects.filter(pk= exam )

    questions_list = Question.objects.filter(exam__pk= exam, )
    question_set = {}

    for word in questions_list:
        question = Question.objects.get(question_text= word, )
        a = question.id
        answer_list = Choice.objects.filter(question__pk = a)
        question_set[word] = list(answer_list)
    answers = zip(answer,correct_answer)
    return render(request, 'exam/review.html', {'question_set':question_set, 'student': smail, 'exam_details':exam_details, 'answer':answers})
