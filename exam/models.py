from django.db import models
from user.models import Year

class Answer(models.Model):
    student_id = models.IntegerField()
    qs_id = models.IntegerField()
    choice_id = models.IntegerField()
    exam_id = models.IntegerField()
        
    def __str__(self):
        return str(self.student_id) +" - " + str(self.qs_id) 

class Exam(models.Model):
    exam_name = models.CharField(max_length=150)
    year = models.ForeignKey(Year, on_delete=models.DO_NOTHING)
    total_marks = models.IntegerField(default=0)
    #start_date_time = models.DateTimeField(blank=True, null=True)
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
    cover = models.ImageField(upload_to='images/questions/', default = None, blank=True, null=True)

    def __str__(self):
        return self.question_text 

    def getChoices(self):
        return Choice.objects.filter(question = self)

    def getChoiceImage(self):
        return ChoiceImage.objects.filter(question = self)
        ch = ChoiceImage.objects.filter(question = self).count()
        if ch != 0:
            return ChoiceImage.objects.filter(question = self)
        else:
            return False

    choice = property(getChoices)
    choiceImage = property(getChoiceImage)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

class ChoiceImage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_cover = models.ImageField(upload_to='images/choices/', default = None, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Mark(models.Model):
    student_id = models.IntegerField(default=1)
    exam_id = models.IntegerField(default=1)
    mark = models.IntegerField(default=1)

    def __str__(self):
        return str(self.student_id) + " - " + str(self.mark)

