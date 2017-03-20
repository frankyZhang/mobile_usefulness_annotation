from django.db import models

# Create your models here.

# MongoEngine	Django
# StringField	CharField
# URLField	URLField
# EmailField	EmailField
# IntField	IntegerField
# FloatField	FloatField
# DecimalField	DecimalField
# BooleanField	BooleanField
# DateTimeField	DateTimeField
# EmbeddedDocumentField	--
# DictField	--
# ListField	--
# SortedListField	--
# BinaryField	--
# ObjectIdField	--
# FileField	FileField


class Setting(models.Model):
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    source = models.CharField(max_length=1000)
    status = models.IntegerField()


class Task(models.Model):
    task_id = models.IntegerField()
    description = models.CharField(max_length=1000)
    init_query = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)


class Results(models.Model):
    task_id = models.IntegerField()
    source = models.CharField(max_length=1000)
    content = models.CharField(max_length=100000000)


class Usefulness(models.Model):
    user_id = models.CharField(max_length=50)
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    result_id = models.IntegerField()
    score = models.IntegerField()


class PreUsefulness(models.Model):
    user_id = models.CharField(max_length=50)
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    result_id = models.IntegerField()
    score = models.IntegerField()
    results_number = models.IntegerField()


class AttUsefulness(models.Model):
    user_id = models.CharField(max_length=50)
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    result_id = models.IntegerField()
    score = models.IntegerField()


class TaskSatisfaction(models.Model):
    user_id = models.CharField(max_length=50)
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    score = models.IntegerField()


class TaskRealism(models.Model):
    user_id = models.CharField(max_length=50)
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    score = models.IntegerField()


class Answer(models.Model):
    user_id = models.CharField(max_length=50)
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    answer = models.CharField(max_length=5000)


if __name__ == '__main__':
    task = Task(connect='hello world', task_id=0)
    task.save()






