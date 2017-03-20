#coding=utf8
__author__ = 'defaultstr'
from anno.models import *
from django.db import transaction, models
import re
import urllib


patterns = {key: re.compile('%s=(.*?)\\t' % key) for key in ['USER', 'SETTING', 'TASK', 'RESULT', 'NUMBER']}
anno_info_patterns = {}
anno_info_patterns['PREUSEFULNESS'] = re.compile('PREUSEFULNESS=(.*?)\\t')
anno_info_patterns['ATTUSEFULNESS'] = re.compile('ATTUSEFULNESS=(.*?)\\t')
anno_info_patterns['USEFULNESS'] = re.compile('\\tUSEFULNESS=(.*?)$')


def from_string(line):
    print line
    setting_id = patterns['SETTING'].search(line).group(1)
    task_id = patterns['TASK'].search(line).group(1)
    results_number = patterns['NUMBER'].search(line).group(1)
    for i in range(int(results_number)):
        anno_info_patterns['URL_'+str(i)] = re.compile('\\tURL_'+str(i)+'=(.*?)\\n')
        try:
            url_ = ''
            url_i = anno_info_patterns['URL_'+str(i)].search(line).group(1)
            urls = url_i.split(',,,')
            for url in urls:
                if url == '':
                    continue
                elif url[0] == '.':
                    url_ += 'http://wap.sogou.com/web' + url[1:] + ',,,'
                elif url[0] == '/':
                    url_ += 'http://m.baidu.com' + url + ',,,'
                else:
                    url_ += url + ',,,'
            print 'hhh'
            anno_log_obj = Url.objects.create(
                setting_id=int(setting_id),
                task_id=int(task_id),
                result_id=int(i),
                url=url_
            )
            anno_log_obj.save()
        except Exception:
            print 'wrong', i


def insert_message(message):
    try:
        from_string(message)
    except Exception:
        transaction.rollback()
    else:
        print "commit success!"
        transaction.commit()
