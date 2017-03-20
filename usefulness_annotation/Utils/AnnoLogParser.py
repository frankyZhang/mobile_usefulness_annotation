#coding=utf8
__author__ = 'defaultstr'
from anno.models import *
from django.db import transaction, models
import re


patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['USER', 'SETTING', 'TASK', 'RESULT', 'NUMBER']}
anno_info_patterns = {}
anno_info_patterns['PREUSEFULNESS'] = re.compile('PREUSEFULNESS=(.*?)\\t')
#anno_info_patterns['ATTUSEFULNESS'] = re.compile('ATTUSEFULNESS=(.*?)\\t')
anno_info_patterns['USEFULNESS'] = re.compile('\\tUSEFULNESS=(.*?)$')


def from_string(line):
    print line
    user_id = patterns['USER'].search(line).group(1)
    setting_id = patterns['SETTING'].search(line).group(1)
    task_id = patterns['TASK'].search(line).group(1)
    result_id = patterns['RESULT'].search(line).group(1)
    results_number = patterns['NUMBER'].search(line).group(1)
    preusefulness = anno_info_patterns['PREUSEFULNESS'].search(line).group(1)
    #attusefulness = anno_info_patterns['ATTUSEFULNESS'].search(line).group(1)
    usefulness = anno_info_patterns['USEFULNESS'].search(line).group(1)
    '''results_usefulness = usefulness.split('\t')
    if int(task_id) != 0:
        print 'hhh'
        for i in range(len(results_usefulness)):
            result_usefulness = results_usefulness[i].split(':')[1]
            print i, result_usefulness
            anno_log_obj = Usefulness.objects.create(
                user_id=user_id,
                setting_id=int(setting_id),
                task_id=int(task_id),
                result_id=i,
                score=int(result_usefulness)
            )
            anno_log_obj.save()'''
    if int(task_id) != 0:
        print 'hhh'
        anno_log_obj = PreUsefulness.objects.create(
            user_id=user_id,
            setting_id=int(setting_id),
            task_id=int(task_id),
            result_id=int(result_id),
            score=int(preusefulness),
            results_number=int(results_number)
        )
        anno_log_obj.save()
        '''anno_log_obj = AttUsefulness.objects.create(
            user_id=user_id,
            setting_id=int(setting_id),
            task_id=int(task_id),
            result_id=int(result_id),
            score=int(attusefulness)
        )
        anno_log_obj.save()'''
        anno_log_obj = Usefulness.objects.create(
            user_id=user_id,
            setting_id=int(setting_id),
            task_id=int(task_id),
            result_id=int(result_id),
            score=int(usefulness)
        )
        anno_log_obj.save()


def insert_message(message):
    try:
        from_string(message)
    except Exception:
        transaction.rollback()
    else:
        print "commit success!"
        transaction.commit()
