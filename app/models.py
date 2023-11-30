from django.db import models

# Create your models here.
class React(models.Model):
    employee = models.CharField(max_Lenght=30)
    department = models.Charfield