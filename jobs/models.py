from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)
    color = models.CharField(max_length=255)


class Company(models.Model):
    img = models.ImageField()
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class Skills(models.Model):
    title = models.CharField(max_length=255)


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, verbose_name='Пароль')
    # enrolled_courses = models.ManyToManyField(Enrolls)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    # USERNAME_FIELD = phone_number

    def __str__(self):
        return self.first_name + " " + self.last_name + " : " + str(self.pk)


class Job(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None)
    title = models.CharField(max_length=255)
    image = models.ImageField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    expires = models.DateTimeField()
    description = models.TextField()
    responsibilities = models.TextField()
    experience = models.TextField()
    skills = models.ManyToManyField(Skills)


class Enrolls(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Job, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField()

