# coding=utf8

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime
from django.template import loader
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, models
import random
from Utils import OutcomeLogParser
from Utils import AnnoLogParser
from Utils import QuerySatisfactionLogParser
from Utils import TaskRealismLogParser
import sys
import urllib
from bs4 import BeautifulSoup
from anno.models import *
from copy import deepcopy
reload(sys)


def login(request):
    settings = set()
    for t in Setting.objects.all():
        settings.add(t.setting_id)

    html = template.Template(open('templates/login.html').read())
    c = template.Context({'settings': settings})
    respon = HttpResponse(html.render(c))
    return HttpResponse(respon)


def training(request, user_id, setting_id):
    all_settings = Setting.objects.filter(setting_id=int(setting_id))
    task = Task.objects.get(task_id=0)
    html = template.Template(open('templates/tasks.html').read())
    c = template.Context({
        'task_id': 0,
        'current_task_num': 0,
        'task_num': len(all_settings),
        'description': task.description,
        'init_query': task.init_query,
        'user_id': user_id,
        'setting_id': setting_id
    })
    respon = HttpResponse(html.render(c))
    return respon


def tasks(request, user_id, setting_id):
    all_settings = Setting.objects.filter(setting_id=int(setting_id))
    finished_relevances = PreUsefulness.objects.filter(user_id=user_id, setting_id=int(setting_id))
    finished_tasks = set()
    for s in finished_relevances:
        if s.task_id:
            task_relevances = PreUsefulness.objects.filter(user_id=user_id, setting_id=int(setting_id), task_id=int(s.task_id))
            if len(task_relevances) >= task_relevances[0].results_number:
                finished_tasks.add(s.task_id)
    if len(all_settings) == len(finished_tasks):
        return HttpResponseRedirect('/tasks/finished/%s/%s/' % (user_id, setting_id))
    unfinished_tasks = []
    for s in all_settings:
        if s.task_id not in finished_tasks:
            unfinished_tasks.append(s.task_id)
    #random.seed(int(user_id)+len(finished_tasks))
    i = random.randint(0, len(unfinished_tasks)-1)
    task = Task.objects.get(task_id=unfinished_tasks[i])
    html = template.Template(open('templates/tasks.html').read())
    c = template.Context({
        'task_id': task.task_id,
        'current_task_num': len(finished_tasks) + 1,
        'task_num': len(all_settings),
        'description': task.description,
        'init_query': task.init_query,
        'user_id': user_id,
        'setting_id': setting_id
    })
    respon = HttpResponse(html.render(c))
    return respon


def tasks_finished(request, user_id, setting_id):
    html = template.Template(open('templates/tasks_finished.html').read())
    c = template.Context({'user_id': user_id, 'setting_id': setting_id})
    respon = HttpResponse(html.render(c))
    return respon


def search(request, user_id, setting_id, task_id):
    task_id = int(task_id)
    setting_id = int(setting_id)
    if task_id:
        setting = Setting.objects.get(setting_id=setting_id, task_id=task_id)
        source = setting.source
    else:
        source = 'baidu'
    task = Task.objects.get(task_id=task_id)
    query = task.init_query
    query_url = urllib.quote(query.encode('utf-8'))
    results = Results.objects.get(task_id=task_id, source=source)
    if source == 'baidu':
        t = template.Template(open('templates/baidu.html').read())
        c = template.Context({
            'is_annotation': False,
            'query_url': query_url,
            'query': query,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))
    elif source == 'sogou':
        t = template.Template(open('templates/sogou.html').read())
        c = template.Context({
            'is_annotation': False,
            'query_url': query_url,
            'query': query,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))
    elif source == 'haosou':
        t = template.Template(open('templates/haosou.html').read())
        c = template.Context({
            'is_annotation': False,
            'query_url': query_url,
            'query': query,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))
    else:
        t = template.Template(open('templates/sm.html').read())
        c = template.Context({
            'is_annotation': False,
            'query_url': query_url,
            'query': query,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))


def taskreview(request, user_id, setting_id, task_id):
    task_id = int(task_id)
    setting_id = int(setting_id)
    task = Task.objects.get(task_id=task_id)
    t = template.Template(open('templates/taskreview.html').read())
    c = template.Context({
        'query': task.init_query,
        'description': task.description,
        'question': task.question,
        'task_id': task.task_id,
        'user_id': user_id,
        'setting_id': setting_id
    })
    return HttpResponse(t.render(c))


def resultsnumber(request, user_id, setting_id, task_id):
    task_id = int(task_id)
    setting_id = int(setting_id)
    if task_id:
        setting = Setting.objects.get(setting_id=setting_id, task_id=task_id)
        source = setting.source
    else:
        source = 'baidu'
    task = Task.objects.get(task_id=task_id)
    query = task.init_query
    query_url = urllib.quote(query.encode('utf-8'))
    results = Results.objects.get(task_id=task_id, source=source)
    if source == 'baidu':
        t = template.Template(open('templates/baidu.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))
    elif source == 'sogou':
        t = template.Template(open('templates/sogou.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))
    elif source == 'haosou':
        t = template.Template(open('templates/haosou.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))
    else:
        t = template.Template(open('templates/sm.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id
        })
        return HttpResponse(t.render(c))


def annotation(request, user_id, setting_id, task_id, results_number):
    task_id = int(task_id)
    setting_id = int(setting_id)
    results_number = int(results_number)
    finished_relevances = Usefulness.objects.filter(user_id=user_id, setting_id=setting_id, task_id=task_id)
    finished_results = set()
    for s in finished_relevances:
        finished_results.add(s.result_id)
    print results_number, len(finished_results)
    if results_number == len(finished_results):
        return HttpResponseRedirect('/tasks/%s/%s/' % (user_id, setting_id))
    unfinished_results = []
    for i in range(results_number):
        if i not in finished_results:
            unfinished_results.append(i)
    i = random.randint(0, len(unfinished_results)-1)
    result_id = unfinished_results[i]

    if task_id:
        setting = Setting.objects.get(setting_id=setting_id, task_id=task_id)
        source = setting.source
    else:
        source = 'baidu'
    task = Task.objects.get(task_id=task_id)

    query = task.init_query
    query_url = urllib.quote(query.encode('utf-8'))
    results = Results.objects.get(task_id=task_id, source=source)
    if source == 'baidu':
        t = template.Template(open('templates/baidu_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id,
            'result_id': result_id,
            'results_number': results_number
        })
        return HttpResponse(t.render(c))
    elif source == 'sogou':
        t = template.Template(open('templates/sogou_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id,
            'result_id': result_id,
            'results_number': results_number
        })
        return HttpResponse(t.render(c))
    elif source == 'haosou':
        t = template.Template(open('templates/haosou_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id,
            'result_id': result_id,
            'results_number': results_number
        })
        return HttpResponse(t.render(c))
    else:
        t = template.Template(open('templates/sm_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task.task_id,
            'user_id': user_id,
            'setting_id': setting_id,
            'result_id': result_id,
            'results_number': results_number
        })
        return HttpResponse(t.render(c))


@csrf_exempt
def log_usefulness(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    AnnoLogParser.insert_message(message)
    return HttpResponse('OK')


@csrf_exempt
def log_outcome(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    OutcomeLogParser.insert_message(message)
    return HttpResponse('OK')


@csrf_exempt
def log_satisfaction(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    QuerySatisfactionLogParser.insert_message(message)
    return HttpResponse('OK')


@csrf_exempt
def log_realism(request):
    message = urllib.unquote(request.POST[u'message'])
    TaskRealismLogParser.insert_message(message)
    return HttpResponse('OK')
