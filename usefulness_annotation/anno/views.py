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
    tasks = set()
    for t in Task.objects.all():
        tasks.add(t.task_id)

    html = template.Template(open('templates/login.html').read())
    c = template.Context({'settings': tasks})
    respon = HttpResponse(html.render(c))
    return HttpResponse(respon)


'''def training(request, user_id, setting_id):
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
    return respon'''


def tasks(request, assessor_id, task_id):
    task_id = int(task_id)
    '''task_session_units = SessionUnit.objects.filter(task_id=task_id)
    task_sessions = set()
    for s in task_session_units:
        task_sessions.add(s.session_id)
    finished_satisfactions = TaskSatisfaction.objects.filter(assessor_id=assessor_id)
    finished_sessions = set()
    for s in finished_satisfactions:
        finished_sessions.add(s.session_id)
    # if len(all_sessions) == len(finished_sessions):
    #     return HttpResponseRedirect('/tasks/finished/%s/%s/' % (assessor_id, str(task_id)))
    unfinished_sessions = []
    for sid in task_sessions:
        if sid not in finished_sessions:
            unfinished_sessions.append(sid)
    if len(unfinished_sessions) == 0:
        return HttpResponseRedirect('/tasks/finished/%s/%s/' % (assessor_id, str(task_id)))
    random.shuffle(unfinished_sessions)
    session_id = unfinished_sessions[0]'''
    task = Task.objects.get(task_id=task_id)

    html = template.Template(open('templates/tasks.html').read())
    c = template.Context({
        'task_id': task_id,
        # 'current_task_num': len(task_sessions) - len(unfinished_sessions) + 1,
        # 'task_num': len(task_sessions),
        'description': task.description,
        'assessor_id': assessor_id,
        # 'session_id': session_id
    })
    respon = HttpResponse(html.render(c))
    return respon


def tasks_finished(request, assessor_id, task_id):
    html = template.Template(open('templates/tasks_finished.html').read())
    c = template.Context({'user_id': assessor_id, 'setting_id': task_id})
    respon = HttpResponse(html.render(c))
    return respon


'''def search(request, user_id, setting_id, task_id):
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
        return HttpResponse(t.render(c))'''


def annotation(request, assessor_id, task_id):
    task_id = int(task_id)
    task_session_units = SessionUnit.objects.filter(task_id=task_id)
    task_sessions = set()
    for s in task_session_units:
        task_sessions.add(s.session_id)
    finished_satisfactions = TaskSatisfaction.objects.filter(assessor_id=assessor_id)
    finished_sessions = set()
    for s in finished_satisfactions:
        finished_sessions.add(s.session_id)
    # if len(all_sessions) == len(finished_sessions):
    #     return HttpResponseRedirect('/tasks/finished/%s/%s/' % (assessor_id, str(task_id)))
    unfinished_sessions = []
    for sid in task_sessions:
        if sid not in finished_sessions:
            unfinished_sessions.append(sid)
    if len(unfinished_sessions) == 0:
        return HttpResponseRedirect('/tasks/finished/%s/%s/' % (assessor_id, str(task_id)))
    random.shuffle(unfinished_sessions)
    session_id = unfinished_sessions[0]

    session_units = SessionUnit.objects.filter(session_id=session_id)
    source = session_units[0].source

    '''session_id = models.IntegerField()
    # user_id = models.CharField(max_length=50)
    task_id = models.IntegerField()
    source = models.CharField(max_length=1000)
    index = models.IntegerField()
    result_id = models.IntegerField()
    dwell_time = models.FloatField()
    url = models.CharField(max_length=100000000)
    exposed_time = models.FloatField()'''

    task = Task.objects.get(task_id=task_id)
    query = task.init_query
    query_url = urllib.quote(query.encode('utf-8'))
    results = Results.objects.get(task_id=task_id, source=source)

    sequential_units = []
    for i in range(len(session_units)):
        sequential_units.append(SessionUnit.objects.get(session_id=session_id, index=i))

    if source == 'baidu':
        t = template.Template(open('templates/baidu_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'assessor_id': assessor_id,
            'current_task_num': len(task_sessions) - len(unfinished_sessions) + 1,
            'task_num': len(task_sessions),
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task_id,
            'session_id': session_id,
            'units': sequential_units
        })
        return HttpResponse(t.render(c))
    elif source == 'sogou':
        t = template.Template(open('templates/sogou_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'assessor_id': assessor_id,
            'current_task_num': len(task_sessions) - len(unfinished_sessions) + 1,
            'task_num': len(task_sessions),
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task_id,
            'session_id': session_id,
            'units': sequential_units
        })
        return HttpResponse(t.render(c))
    elif source == 'haosou':
        t = template.Template(open('templates/haosou_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'assessor_id': assessor_id,
            'current_task_num': len(task_sessions) - len(unfinished_sessions) + 1,
            'task_num': len(task_sessions),
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task_id,
            'session_id': session_id,
            'units': sequential_units
        })
        return HttpResponse(t.render(c))
    else:
        t = template.Template(open('templates/sm_annotation.html').read())
        c = template.Context({
            'is_annotation': True,
            'assessor_id': assessor_id,
            'current_task_num': len(task_sessions) - len(unfinished_sessions) + 1,
            'task_num': len(task_sessions),
            'query_url': query_url,
            'query': query,
            'description': task.description,
            'results': results.content,
            'task_id': task_id,
            'session_id': session_id,
            'units': sequential_units
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
