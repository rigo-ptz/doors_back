from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    last_name = models.CharField(max_length=100, verbose_name="Отчество")
    document_number = models.CharField(max_length=25, verbose_name="Номер документа")
    phone_number = models.CharField(max_length=16, verbose_name="Номер телефона")
    email = models.CharField(max_length=200, verbose_name="e-mail", default="")
    pin_code = models.CharField(max_length=4, verbose_name="PIN-код")

    def __str__(self):
        return "{0} {1} {2}".format(self.surname, self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Room(models.Model):
    number = models.DecimalField(max_digits=3, decimal_places=0)
    floor = models.DecimalField(max_digits=1, decimal_places=0)

    def __str__(self):
        return "Кабинет № {0}".format(self.number)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class KeyCell(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    has_key = models.BooleanField(verbose_name="Ключ в ячейке?")

    def __str__(self):
        return "Ячейка для кабинета № {0}".format(self.room.number)

    class Meta:
        verbose_name = 'Ячейка'
        verbose_name_plural = 'Ячейки'


class LogTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key_ceil = models.ForeignKey(KeyCell, on_delete=models.CASCADE)
    log_time = models.DateTimeField(verbose_name="Время")
    EVENTS = (
        ("get_key", "Взял ключ"),
        ("return_key", "Вернул ключ")
        # ("book_key", "Забронировал ключ")
    )
    event = models.CharField(max_length=50, choices=EVENTS, verbose_name="Событие")

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
