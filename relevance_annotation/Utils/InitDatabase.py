__author__ = 'franky'

from anno.models import Task
from anno.models import Setting


def import_tasks(filename):
    print 'import tasks', filename
    fin = open(filename, 'r').readlines()
    for line in fin:
        print line
        task_id, init_query, description, question = line.strip().split('\t')
        task_id = int(task_id)
        t = Task(task_id=task_id, init_query=init_query, question=question, description=description)
        t.save()


def import_settings(filename):
    setting_id = 0
    print 'import settings', filename
    fin = open(filename, 'r').readlines()
    print fin
    for line in fin:
        print line
        setting_id += 1
        task_id = 0
        segs = line.strip().split(',')
        for s in segs:
            task_id += 1
            source = ''
            if s == '1':
                source = 'sogou'
            if s == '2':
                source = 'baidu'
            if s == '3':
                source = 'sm'
            if s == '4':
                source = 'haosou'
            setting = Setting(setting_id=setting_id, task_id=task_id, source=source, status=0)
            setting.save()


def init_default():
    import_tasks('temp/tasks.csv')
    import_settings('temp/setting.csv')
