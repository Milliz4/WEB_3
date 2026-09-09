from django.db import models

# Create your models here.
class Customers(models.Model):
    name = models.TextField("ФИО")
    group_name = models.TextField("Название группы")

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
