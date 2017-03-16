#coding=utf8
__author__ = 'luocheng'
__date__ = '22/12/2016-12:31 AM'
import sys
reload(sys)
sys.setdefaultencoding('utf8')

result_folder_name = '../result/20170118'
new_metric_names = [#'pbg_tbg_orig',
                    #'npbg_tbg_orig',
                    'pbg_tbg_modi',
                    #'pbg_hcs_orig',
                    #'npbg_hcs_orig',
                    'pbg_hcs_modi']
not_normalized_metrics = ['pbg_tbg_modi',  'pbg_hcs_modi'  ]


def parse_result_file(filename):
    # dict in dict    first topic_id, second metric_name
    scores = dict()
    for l in open(filename):
        if '#' in l:
            continue
        else:

            topic_id = l.strip().split(' ')[0]
            if topic_id not in scores:
                scores[topic_id] = dict()
            metric_name = l.strip().split(' ')[1].replace('=', '')
            metric_value = float(l.strip().split(' ')[-1])
            scores[topic_id][metric_name] = float(metric_value)
    filter = filename.split('/')[-1].split('.')[0].lower()

    # for l in open('../newdata/metrics.tsv').readlines():
    #     metric, tag, value = l.strip().split('\t')
    #     qid, source = tag.split('.')
    #     value = float(value)
    #     if source == filter:
    #         scores[qid][metric] = value
    for metric in new_metric_names:
        for l in open('../newdata/'+metric+'.tsv').readlines():
            qid, source, value = l.strip().split('\t')
            value = float(value)
            if source==filter:
                scores[qid][metric] = value
    return scores


# we are going to do two different things here:
#     1. we want to analysis the inner-agreement between different metrics.
#     2. we are going to analysis the agreement between sogou v.s. others. Agree rate.

from scipy.stats.stats import pearsonr
from scipy.stats.stats import kendalltau
from utils import load_content

contents = load_content()

SM = parse_result_file('../data/ntcireval/SM.test.nev')
SOGOU = parse_result_file('../data/ntcireval/SOGOU.test.nev')
HAOSOU = parse_result_file('../data/ntcireval/HAOSOU.test.nev')
BAIDU = parse_result_file('../data/ntcireval/BAIDU.test.nev')

metric_set = SM['0001'].keys()

metric_list = list(metric_set)
metric_list.sort()

fout = open(result_folder_name+'/all_metric_consistency.tsv', 'w')
fout.write('dumb\t')
fout.write('\t'.join(metric_list) + '\n')
for i in range(0, len(metric_list), 1):
    consist = []
    consist.append(metric_list[i])
    for j in range(0, len(metric_list), 1):
        if True:
            m1 = metric_list[i]
            m2 = metric_list[j]

            topics = list(SM.keys())
            import numpy
            import math
            # l1 = [numpy.mean([run[t][m1] for t in topics]) for run in [BAIDU, SOGOU, SM, HAOSOU]]
            # l2 = [numpy.mean([run[t][m2] for t in topics]) for run in [BAIDU, SOGOU, SM, HAOSOU]]

            _consist_topics = []
            for t in topics:
                l1 = [run[t][m1] for run in [BAIDU, SOGOU, SM, HAOSOU]]
                l2 = [run[t][m2] for run in [BAIDU, SOGOU, SM, HAOSOU]]
                _c = kendalltau(l1, l2)[0]

                if math.isnan(_c) == False:
                    _consist_topics.append(_c)

            consist.append(str(numpy.mean(_consist_topics)))
    fout.write('\t'.join(consist) + '\n')
fout.close()

query2id = dict()
for l in open('../data/query.idx'):
    segs = l.strip().split('\t')
    query, id = segs
    query2id[query] = id


from collections import defaultdict

consistent = defaultdict(lambda: 0)
inconsistent = defaultdict(lambda: 0)

metric_set = SM['0001'].keys()
metric_list = list(metric_set)

sbs_data = [item for item in contents if ((item[-5] != 'None') and (item[-5] != 'sogou') and (item[-5] != ''))]

# user preference:  (qid, source) = sbs

sbs_preference = dict()
details = defaultdict(lambda: '')
for item in sbs_data:
    query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments,_ = item[0:11]
    queryid = query2id[query]
    print query,queryid

    A = SOGOU
    if source == 'baidu':
        B = BAIDU
    elif source == 'sm':
        B = SM
    elif source == 'haosou':
        B = HAOSOU

    if '-' in sbs or sbs.isdigit():
        sbs_preference[(queryid,source)] = int(sbs)
    for m in metric_list:
        A[queryid][m] = round(A[queryid][m], 3)
        B[queryid][m] = round(B[queryid][m], 3)

        if m in not_normalized_metrics:
            if abs(A[queryid][m] - B[queryid][m]) < 0.05*max(A[queryid][m], B[queryid][m]):
                if int(sbs) == 0:
                    consistent[m]+=1
                    details[(queryid, source, m)] = 'CONSIST|'+str(A[queryid][m])+'|' +str(B[queryid][m])
                else:
                    inconsistent[m]+=1
                    if int(sbs) == 0:
                        details[(queryid, source, m)] += 'P='
                    elif int(sbs) > 0:
                        details[(queryid, source, m)] += 'P>'
                    else:
                        details[(queryid, source, m)] += 'P<'

                    details[(queryid, source, m)] +='M='+'|'+str(A[queryid][m])+'|' +str(B[queryid][m])

            else:
                if (A[queryid][m] < B[queryid][m] and int(sbs) < 0) or ( A[queryid][m] > B[queryid][m] and int(sbs) > 0):
                    consistent[m]+=1
                    details[(queryid, source, m)] = 'CONSIST|'+str(A[queryid][m])+'|' +str(B[queryid][m])
                else:
                    inconsistent[m]+=1
                    if int(sbs) == 0:
                        details[(queryid, source, m)] += 'P='
                    elif int(sbs) > 0:
                        details[(queryid, source, m)] += 'P>'
                    else:
                        details[(queryid, source, m)] += 'P<'
                    if A[queryid][m] < B[queryid][m]:
                        details[(queryid, source, m)] += 'M<'+'|'+str(A[queryid][m])+'|' +str(B[queryid][m])
                    if A[queryid][m] > B[queryid][m]:
                        details[(queryid, source, m)] += 'M>'+'|'+str(A[queryid][m])+'|' +str(B[queryid][m])


        else:
            if abs(A[queryid][m] - B[queryid][m]) < 0.05:
                if int(sbs) == 0:
                    consistent[m]+=1
                    details[(queryid, source, m)] = 'CONSIST|'+str(A[queryid][m])+'|' +str(B[queryid][m])
                else:
                    inconsistent[m]+=1
                    if int(sbs) == 0:
                        details[(queryid, source, m)] += 'P='
                    elif int(sbs) > 0:
                        details[(queryid, source, m)] += 'P>'
                    else:
                        details[(queryid, source, m)] += 'P<'

                    details[(queryid, source, m)] +='M='+'|'+str(A[queryid][m])+'|' +str(B[queryid][m])

            else:
                if (A[queryid][m] < B[queryid][m] and int(sbs) < 0) or ( A[queryid][m] > B[queryid][m] and int(sbs) > 0):
                    consistent[m]+=1
                    details[(queryid, source, m)] = 'CONSIST|'+str(A[queryid][m])+'|' +str(B[queryid][m])
                else:
                    inconsistent[m]+=1
                    if int(sbs) == 0:
                        details[(queryid, source, m)] += 'P='
                    elif int(sbs) > 0:
                        details[(queryid, source, m)] += 'P>'
                    else:
                        details[(queryid, source, m)] += 'P<'
                    if A[queryid][m] < B[queryid][m]:
                        details[(queryid, source, m)] += 'M<'+'|'+str(A[queryid][m])+'|' +str(B[queryid][m])
                    if A[queryid][m] > B[queryid][m]:
                        details[(queryid, source, m)] += 'M>'+'|'+str(A[queryid][m])+'|' +str(B[queryid][m])


            # if details[(queryid,source,m)] != 'CONSIST' and len(details[(queryid,source,m)] ) != 4:
            #     print source, queryid,A[queryid][m],m , B[queryid][m],sbs,details[(queryid,source,m)]

fout = open(result_folder_name+'/consistent_rate_metric.tsv', 'w')

output = [(m,float(consistent[m]), float(inconsistent[m]))  for m in consistent]
output.sort(key=lambda x:x[1], reverse=True)

for m in output:
    fout.write(m[0]+'\t'+str(m[1])+'\t'+str(m[2])+'\n')
fout.close()

focus = defaultdict(lambda: '')
for compare in ['baidu','sm','haosou']:
    fout = open(result_folder_name+'/detail_metric_sbs.'+compare+'.tsv','w')
    queries = [query2id[item]+':'+item for item in query2id]
    queries.sort()

    fout.write('Metric\t'+'\t'.join(queries)+'\n')
    for m in metric_list:

        fout.write(m+'\t')
        queryids = [item.split(':')[0] for item in queries]
        fout.write('\t'.join([details[(q,compare,m)] for q in queryids]))
        for q in queryids:
            if m == 'pbg_hcs_modi':
                focus[(compare, q)] = details[(q,compare,m)]
        fout.write('\n')
    fout.close()


pbghcsout = open(result_folder_name+'/focus_pbg_hcs_modi.tsv','w')

pbghcsout.write('dumb\tbaidu\thaosou\tsm\n')
for q in range(1,51,1):
    qid = '0'*(4-len(str(q)))+ str(q)
    pbghcsout.write('\t'.join([qid] + [focus[(c,qid)] for c in ['baidu','haosou','sm']]))
    pbghcsout.write('\n')
pbghcsout.close()



# merge tsv files
from openpyxl import Workbook
wb = Workbook(write_only=True)

for source in ['baidu', 'haosou', 'sm']:
    ws = wb.create_sheet(source)
    for l in open(result_folder_name+'/detail_metric_sbs.'+source+'.tsv').readlines():
        ws.append(l.strip().split('\t'))


wb.save(result_folder_name+'/merge.xlsx')
