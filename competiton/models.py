from django.db import models

class Profession(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    profession = models.ForeignKey(
        to=Profession,
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.last_name: return f'{self.first_name} {self.last_name}'
        return self.first_name
    

class Group(models.Model):
    name = models.CharField(max_length=64)
    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
    

class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE
    )
    telegram_chat_id = models.CharField(max_length=9, unique=True)
    telegram_username = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        if self.last_name: return f'{self.first_name} {self.last_name} in {self.group.name}'
        return f'self.first_name in {self.group.name}'
    

class Stage(models.Model):
    step = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.step


class Result(models.Model):
    stage = models.ForeignKey(
        to=Stage,
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stage} - {self.student}'
    
