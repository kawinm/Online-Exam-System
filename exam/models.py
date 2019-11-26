from django.db import models
from user.models import Year

class Exam(models.Model):
    exam_name = models.CharField(max_length=150)
    year = models.ForeignKey(Year, on_delete=models.DO_NOTHING)
    total_marks = models.IntegerField(default=0)
    start_date_time = models.DateTimeField(blank=True, null=True)
    total_time = models.IntegerField(default=0, help_text="Enter in minutes")
    active = models.BooleanField(default=False, blank = True)

    class meta():
        ordering = ('start_date_time','exam_name')
        
    def __str__(self):
        return self.exam_name

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    question_text = models.CharField(max_length=200)
    correct_answer = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text 

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text