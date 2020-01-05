from django.contrib import admin
from django.urls import path, include

from exam import views

app_name = 'exam'
urlpatterns = [
    path('mark/exam=<int:exam>/student=<int:student>', views.calculate_mark, name='calculate_mark'),
    path('exam/exam_id=<int:pk>', views.take_exam, name='take_exam'),
    path('review/exam_id=<int:exam>/student=<int:student>', views.review_exam, name='review_exam'),
    path('exam/pdf/exam_id=<int:exam>', views.generate_pdf, name='generate_pdf'),
    path('admin/exam/question/add_questions', views.add_questions, name="add_questions"),
    path('', views.main, name='main'),
]