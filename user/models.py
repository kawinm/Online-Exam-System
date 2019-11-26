from django.db import models

class Year(models.Model):

    YEAR = (
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
        (5, 'Fifth Year')
    )

    year      = models.IntegerField(
        choices=YEAR,
    )
    total_students = models.IntegerField()

    def __str__(self):
        message = self.get_year_display()
        return message

class Student(models.Model):
    
    first_name = models.CharField(max_length = 150)
    last_name  = models.CharField(max_length = 150)
    year      = models.ForeignKey(Year, on_delete = models.DO_NOTHING)

    email_id   = models.EmailField()
    password   = models.CharField(max_length=255)
    
    def __str__(self):
        message = self.first_name + ' ' + self.last_name + ' (' + str(self.year) + ')'
        return message
