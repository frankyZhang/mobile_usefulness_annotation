# coding=utf8
__author__ = 'defaultstr'
from anno.models import *
from django.db import transaction, models
import re


patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['ASSESSOR', 'SESSION']}
anno_info_patterns = {}
anno_info_patterns['SATISFACTION'] = re.compile('SATISFACTION=(.*?)$')


def from_string(line):
    print line
    assessor_id = patterns['ASSESSOR'].search(line).group(1)
    session_id = patterns['SESSION'].search(line).group(1)
    satisfaction = anno_info_patterns['SATISFACTION'].search(line).group(1)
    print satisfaction

    print 'satisfaction'
    anno_log_obj = TaskSatisfaction.objects.create(
        assessor_id=assessor_id,
        session_id=int(session_id),
        score=int(satisfaction)
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
