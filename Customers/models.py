from django.db import models


class Group(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

class Customer(models.Model):
    name = models.TextField("ФИО")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def str(self) -> str:
        return self.name
