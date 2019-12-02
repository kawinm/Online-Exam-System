from django.contrib import admin

from exam.models import Exam, Question, Choice, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('exam', 'question_text', 'correct_answer')
    

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Exam)
admin.site.register(Answer)
