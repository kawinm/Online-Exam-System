from django.contrib import admin

from user.models import Student, Year

class StudentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user/add_student.html'

admin.site.register(Student, StudentAdmin)
admin.site.register(Year)
