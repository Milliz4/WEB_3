from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    class Role(models.IntegerChoices):
        undefined = 0, "Не определена"
        customer = 1, "Покупатель"
        administrator = 2, "Администратор"

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    role = models.IntegerField("Роль", choices=Role, default=Role.undefined)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username if self.user else f"Profile {self.id}"


@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance, role=Profile.Role.undefined)


class Customer(models.Model):
    full_name = models.TextField("ФИ")
    email = models.TextField("Email")
    phone = models.TextField("Телефон")

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self) -> str:
        return self.full_name


class Address(models.Model):
    customer = models.ForeignKey(
        "products.Customer", on_delete=models.CASCADE, null=True, verbose_name="Покупатель"
    )
    street = models.TextField("Улица")
    city = models.TextField("Город")
    postal_code = models.TextField("Почтовый индекс")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self) -> str:
        return f"{self.city}, {self.street}"


class Category(models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Manufacturer(models.Model):
    name = models.TextField("Название")
    country = models.TextField("Страна")
    # картинка №2 для задания 3 (логотип производителя)
    picture = models.ImageField("Логотип", null=True, blank=True, upload_to="manufacturers/")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        "products.Category", on_delete=models.CASCADE, null=True, verbose_name="Категория"
    )
    manufacturer = models.ForeignKey(
        "products.Manufacturer", on_delete=models.CASCADE, null=True, verbose_name="Производитель"
    )
    name = models.TextField("Название")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Остаток на складе", default=0)
    # картинка №1 для задания 3 (главное фото товара)
    picture = models.ImageField("Изображение", null=True, blank=True, upload_to="products/")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return self.name


# Задание 4: к одному товару можно привязать много фотографий (альбом)
class ProductPhoto(models.Model):
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, null=True, verbose_name="Товар"
    )
    image = models.ImageField("Фото", upload_to="product_photos/")

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"

    def __str__(self) -> str:
        return f"Фото {self.id} — {self.product}"


class Order(models.Model):
    customer = models.ForeignKey(
        "products.Customer", on_delete=models.CASCADE, null=True, verbose_name="Покупатель"
    )
    address = models.ForeignKey(
        "products.Address", on_delete=models.CASCADE, null=True, verbose_name="Адрес доставки"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class StatusType(models.TextChoices):
        CREATED = "CREATED", "Создан"
        PAID = "PAID", "Оплачен"
        DELIVERED = "DELIVERED", "Доставлен"
        CANCELLED = "CANCELLED", "Отменён"

    status = models.TextField("Статус", choices=StatusType.choices, default=StatusType.CREATED)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"Заказ #{self.id} — {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "products.Order", on_delete=models.CASCADE, null=True, verbose_name="Заказ"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, null=True, verbose_name="Товар"
    )
    quantity = models.IntegerField("Количество", default=1)
    price = models.DecimalField("Цена на момент заказа", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self) -> str:
        return f"{self.product} x{self.quantity}"


class Review(models.Model):
    customer = models.ForeignKey(
        "products.Customer", on_delete=models.CASCADE, null=True, verbose_name="Покупатель"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, null=True, verbose_name="Товар"
    )
    rating = models.IntegerField(
        "Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField("Текст отзыва")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        return f"{self.customer} о {self.product}"