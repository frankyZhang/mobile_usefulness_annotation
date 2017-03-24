#coding=utf8
__author__ = 'defaultstr'
from anno.models import *
from django.db import transaction, models
import re


patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['ASSESSOR', 'SESSION']}
anno_info_patterns = {}
# anno_info_patterns['PREUSEFULNESS'] = re.compile('PREUSEFULNESS=(.*?)\\t')
# anno_info_patterns['ATTUSEFULNESS'] = re.compile('ATTUSEFULNESS=(.*?)\\t')
anno_info_patterns['USEFULNESS'] = re.compile('\\tUSEFULNESS=\\t(.*?)$')


def from_string(line):
    print line
    assessor_id = patterns['ASSESSOR'].search(line).group(1)
    session_id = patterns['SESSION'].search(line).group(1)
    usefulness = anno_info_patterns['USEFULNESS'].search(line).group(1)
    results_usefulness = usefulness.split('\t')

    print 'usefulness'
    for i in range(len(results_usefulness)):
        result_usefulness = results_usefulness[i].split(':')[1]
        print i, result_usefulness
        anno_log_obj = Usefulness.objects.create(
            assessor_id=assessor_id,
            session_id=int(session_id),
            index=i,
            score=int(result_usefulness)
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
