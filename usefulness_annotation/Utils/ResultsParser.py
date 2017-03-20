__author__ = 'franky'
# coding=utf8

from anno.models import Results
from bs4 import BeautifulSoup


def import_baidu_results(task_id, filename):
    results = open(filename).read()
    r = Results(task_id=task_id, source='baidu', content=results)
    r.save()


def import_sogou_results(task_id, filename):
    results = open(filename).read()
    r = Results(task_id=task_id, source='sogou', content=results)
    r.save()


def import_haosou_results(task_id, filename):
    results = open(filename).read()
    r = Results(task_id=task_id, source='haosou', content=results)
    r.save()


def import_sm_results(task_id, filename):
    results = open(filename).read()
    r = Results(task_id=task_id, source='sm', content=results)
    r.save()


def import_results():
    tasks = open('temp/tasks.csv', 'r').readlines()
    for line in tasks:
        print line
        task_id, init_query, description, question = line.strip().split('\t')
        task_id = int(task_id)
        import_baidu_results(task_id, 'serps/baidu_serp/'+init_query+'.html')
        import_sogou_results(task_id, 'serps/sogou_serp/'+init_query+'.html')
        import_haosou_results(task_id, 'serps/haosou_serp/'+init_query+'.html')
        import_sm_results(task_id, 'serps/sm_serp/'+init_query+'.html')
