from django.contrib import admin
from django.urls import path, include

from exam import views

app_name = 'exam'
urlpatterns = [
    path('mark/<int:exam>/<int:student>', views.calculate_mark, name='calculate_mark'),
    path('exam/<int:pk>', views.take_exam, name='take_exam'),
    path('', views.main, name='main'),
]