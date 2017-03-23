__author__ = 'franky'

from anno.models import Task, SessionUnit
# from anno.models import Setting


def import_tasks(filename):
    print 'import tasks', filename
    fin = open(filename, 'r').readlines()
    for line in fin:
        print line
        task_id, init_query, description, question = line.strip().split('\t')
        task_id = int(task_id)
        t = Task(task_id=task_id, init_query=init_query, question=question, description=description)
        t.save()


'''def import_settings(filename):
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
            setting.save()'''


def import_sessions(filename):
    print 'import sessions', filename
    fin = open(filename, 'r').readlines()[1:]
    for line in fin:
        print line
        id,session_id,user_id,setting_id,task_id,source_id,annotation_index,result_id,timestamp,is_clicked,click_dwell_time,clicked_url,weighted_exposed_time = line.strip().split('\t')
        session_id = int(session_id)
        task_id = int(task_id)
        source = ''
        if source_id == '1':
            source = 'sogou'
        if source_id == '2':
            source = 'baidu'
        if source_id == '3':
            source = 'sm'
        if source_id == '4':
            source = 'haosou'
        index = int(annotation_index)
        result_id = int(result_id)
        dwell_time = float(click_dwell_time)
        exposed_time = float(weighted_exposed_time)
        s = SessionUnit(session_id=session_id, task_id=task_id, source=source, index=index, result_id=result_id, dwell_time=dwell_time, url=clicked_url, exposed_time=exposed_time)
        s.save()


def init_default():
    import_tasks('temp/tasks.csv')
    import_sessions('temp/annotation_sequence.tsv')
    # import_settings('temp/setting.csv')
