from django.db import models

# Create your models here.
class EmployeeModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    age = models.IntegerField()

    def __str__(self):
        return self._meta.get_fields()

    @property
    def is_authenticated(self):
        return True
