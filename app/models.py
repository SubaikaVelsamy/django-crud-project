from django.db import models

# Create your models here.
class Student(models.Model):
    STATUS_CHOICES = [
        ('Y', 'Active'),
        ('N', 'Inactive'),
    ]

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    email = models.CharField(max_length=100)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='Y')

    class Meta:
        db_table = "student_data"
        managed=False

    def __str__(self):
        return self.full_name

