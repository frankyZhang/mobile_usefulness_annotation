# coding=utf8
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


'''class Setting(models.Model):
    setting_id = models.IntegerField()
    task_id = models.IntegerField()
    source = models.CharField(max_length=1000)
    status = models.IntegerField()'''


class Task(models.Model):
    task_id = models.IntegerField()
    description = models.CharField(max_length=1000)
    init_query = models.CharField(max_length=1000)
    question = models.CharField(max_length=1000)


class Results(models.Model):
    task_id = models.IntegerField()
    source = models.CharField(max_length=1000)
    content = models.CharField(max_length=100000000)


# 标注的单元为一个session,包含若干units
class SessionUnit(models.Model):
    session_id = models.IntegerField()
    # user_id = models.CharField(max_length=50)
    task_id = models.IntegerField()
    source = models.CharField(max_length=1000)
    index = models.IntegerField()
    result_id = models.IntegerField()
    dwell_time = models.FloatField()
    url = models.CharField(max_length=100000000)
    exposed_time = models.FloatField()


# 我们最后得到的单元是某个assessor对某个session的某个result的usefulness标注(result可能重复出现)
class Usefulness(models.Model):
    assessor_id = models.CharField(max_length=50)
    session_id = models.IntegerField()
    # user_id = models.CharField(max_length=50)
    # setting_id = models.IntegerField()
    # task_id = models.IntegerField()
    # source = models.CharField(max_length=1000)
    index = models.IntegerField()
    # result_id = models.IntegerField()
    score = models.IntegerField()


# 我们最后得到的单元是某个assessor对某个session的satisfaction标注
class TaskSatisfaction(models.Model):
    assessor_id = models.CharField(max_length=50)
    session_id = models.IntegerField()
    # user_id = models.CharField(max_length=50)
    # task_id = models.IntegerField()
    # source = models.CharField(max_length=1000)
    score = models.IntegerField()


if __name__ == '__main__':
    task = Task(connect='hello world', task_id=0)
    task.save()






