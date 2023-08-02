from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='изображение')
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)
    price = models.IntegerField(default=1000, verbose_name='стоимость курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='изображение')
    video = models.URLField(**NULLABLE, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_METHOD_CASH = 'cash'
    PAYMENT_METHOD_TRANSFER = 'transfer'
    PAYMENT_METHOD_CHOICES = (
        (PAYMENT_METHOD_CASH, 'Наличные'),
        (PAYMENT_METHOD_TRANSFER, 'Перевод на счет'),
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    lesson_pay = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплата урока')
    course_pay = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='оплата курса')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')
    payment_intent_id = models.CharField(max_length=500, **NULLABLE, verbose_name='ID намерения платежа')
    payment_method_id = models.CharField(max_length=500, **NULLABLE, verbose_name='ID метода платежа')
    status = models.CharField(max_length=50, **NULLABLE, verbose_name='cтатус платежа')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"Платеж от пользователя: {self.user} дата: {self.date} на сумму {self.amount} ({self.payment_method})"


class Subscription(models.Model):
    status = models.BooleanField(default=True, verbose_name='Статус подписки')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
