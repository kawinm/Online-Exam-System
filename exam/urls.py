from django.contrib import admin
from django.urls import path, include

from exam import views

app_name = 'exam'
urlpatterns = [
    path('exam/<int:pk>', views.take_exam, name='take_exam'),
    path('', views.main, name='main'),
]