from django.db import models
from django.core.validators import RegexValidator

class Year(models.Model):

    YEAR = (
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
        (5, 'Fifth Year')
    )

    year  = models.IntegerField(
        choices=YEAR,
    )
    total_students = models.IntegerField()

    def __str__(self):
        message = self.get_year_display()
        return message

def get_image_path(instance, filename):
    return os.path.join('photos', filename)

class Student(models.Model):

    #RegexValidator used to check the given fields contain only alphanumeric characters
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    first_name = models.CharField(max_length = 150, validators=[alphanumeric])
    last_name  = models.CharField(max_length = 150, validators=[alphanumeric])
    year      = models.ForeignKey(Year, on_delete = models.DO_NOTHING)

    is_active = models.BooleanField(default=False)
    email_id   = models.EmailField()
    password   = models.CharField(max_length=255)

    def __str__(self):
        message = self.first_name + ' ' + self.last_name + ' (' + str(self.year) + ')'
        return message
