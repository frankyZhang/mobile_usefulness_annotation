#coding=utf8
__author__ = 'defaultstr'
from anno.models import *
from django.db import transaction, models
import re


patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['USER', 'SETTING', 'TASK']}
anno_info_patterns = {}
anno_info_patterns['REALISM'] = re.compile('REALISM=(.*?)$')


def from_string(line):
    print line
    user_id = patterns['USER'].search(line).group(1)
    setting_id = patterns['SETTING'].search(line).group(1)
    task_id = patterns['TASK'].search(line).group(1)
    realism = anno_info_patterns['REALISM'].search(line).group(1)
    print realism
    if int(task_id) != 0:
        print 'hhh'
        anno_log_obj = TaskRealism.objects.create(
            user_id=user_id,
            setting_id=int(setting_id),
            task_id=int(task_id),
            score=int(realism)
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
