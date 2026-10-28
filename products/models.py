from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField("Название")
    description = models.TextField("Описание", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Остаток на складе", default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Order(models.Model):
    class StatusType(models.TextChoices):
        CREATED = "CREATED", "Создан"
        PAID = "PAID", "Оплачен"
        DELIVERED = "DELIVERED", "Доставлен"
        CANCELLED = "CANCELLED", "Отменён"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Наличные"
        CARD_ONLINE = "CONLINE", "Картой онлайн"
        CARD_COURIER = "CCOURIER", "Картой курьеру"

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Покупатель",
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    status = models.TextField(
        "Статус",
        choices=StatusType,
        default=StatusType.CREATED
    )
    total = models.DecimalField("Сумма заказа", max_digits=10, decimal_places=2)
    payment_method = models.TextField(
        "Способ оплаты",
        choices=PaymentMethod,
        default=PaymentMethod.CASH
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} — {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    quantity = models.IntegerField("Количество", default=1)
    price = models.DecimalField("Цена на момент заказа", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product} x{self.quantity}"


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Автор",
    )
    rating = models.IntegerField("Оценка")
    text = models.TextField("Текст отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв на {self.product}"