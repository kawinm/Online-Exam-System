from django.contrib import admin

from exam.models import Exam, Question, Choice, Answer, ChoiceImage
from django.contrib.auth.models import Group

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class ChoiceImageInline(admin.TabularInline):
    model = ChoiceImage
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline, ChoiceImageInline]
    list_display = ('exam', 'question_text', 'correct_answer')
    change_list_template = 'admin/exam/question_add_list.html'
    

admin.site.register(Question, QuestionAdmin)
admin.site.register(Exam)

admin.site.unregister(Group)
