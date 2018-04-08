from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
import pytz


class DoorsUserManager(BaseUserManager):
    def create_user(
            self,
            first_name,
            surname,
            last_name,
            document_number,
            phone_number,
            email,
            pin_code,
            password=None
    ):
        """
        Creates and saves a User with the given data
        """
        if not email:
            raise ValueError("Не указан e-mail")

        if not phone_number:
            raise ValueError("Не указан телефон")

        if not pin_code:
            raise ValueError("Не указан PIN-код")

        user = self.model(
            first_name=first_name,
            surname=surname,
            last_name=last_name,
            document_number=document_number,
            phone_number=phone_number,
            email=email,
            pin_code=pin_code,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            email=email,
            password=password,
        )
        user.set_password(password)
        user.active = True
        user.is_superuser = True
        user.staff = True
        user.save(using=self._db)
        return user


class DoorsUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    last_name = models.CharField(max_length=100, verbose_name="Отчество")
    document_number = models.CharField(max_length=25, verbose_name="Номер документа")
    phone_number = models.CharField(max_length=16, verbose_name="Номер телефона")
    email = models.CharField(max_length=200, verbose_name="e-mail", unique=True)
    pin_code = models.CharField(max_length=4, verbose_name="PIN-код")
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False, verbose_name="Доступ к админке?")

    USERNAME_FIELD = 'email'

    objects = DoorsUserManager()

    def __str__(self):
        return "{0} {1} {2}".format(self.surname, self.first_name, self.last_name)

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active

    # this methods are require to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return self.is_staff

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class User(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    last_name = models.CharField(max_length=100, verbose_name="Отчество")
    document_number = models.CharField(max_length=25, verbose_name="Номер документа")
    phone_number = models.CharField(max_length=16, verbose_name="Номер телефона")
    email = models.CharField(max_length=200, verbose_name="e-mail", default="")
    pin_code = models.CharField(max_length=4, verbose_name="PIN-код")
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return "{0} {1} {2}".format(self.surname, self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Room(models.Model):
    number = models.DecimalField(max_digits=3, decimal_places=0, verbose_name="Номер кабинета")
    floor = models.DecimalField(max_digits=1, decimal_places=0, verbose_name="Этаж")

    def __str__(self):
        return "Кабинет № {0}".format(self.number)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class KeyCell(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    has_key = models.BooleanField(verbose_name="Ключ в ячейке?")
    user_who_get = models.ForeignKey(DoorsUser, on_delete=models.CASCADE, default=None, blank=True, null=True, verbose_name="Кто взял ключ")

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


class Lesson(models.Model):
    time_start = models.DateTimeField(verbose_name="Время начала")
    time_end = models.DateTimeField(verbose_name="Время окончания")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(DoorsUser, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "Занятие"

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

