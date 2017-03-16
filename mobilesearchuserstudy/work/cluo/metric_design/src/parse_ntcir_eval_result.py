# coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from openpyxl import load_workbook


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
    for l in open('../newdata/metrics.tsv').readlines():
        metric, tag, value = l.strip().split('\t')
        qid, source = tag.split('.')
        value = float(value)
        if source == filter:
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
#
# metric_set = SM['0001'].keys()
# metric_list = list(metric_set)
# metric_list.sort()
#
# fout = open('../data/consistency.tsv', 'w')
# fout.write('dumb\t')
# fout.write('\t'.join(metric_list) + '\n')
# for i in range(0, len(metric_list), 1):
#     consist = []
#     consist.append(metric_list[i])
#     for j in range(0, len(metric_list), 1):
#         if j < i:
#             consist.append('')
#         else:
#             m1 = metric_list[i]
#             m2 = metric_list[j]
#
#             topics = list(SM.keys())
#             import numpy
#
#             l1 = [numpy.mean([run[t][m1] for t in topics]) for run in [BAIDU, SOGOU, SM, HAOSOU]]
#
#             l2 = [numpy.mean([run[t][m2] for t in topics]) for run in [BAIDU, SOGOU, SM, HAOSOU]]
#
#             from scipy.stats import kendalltau
#             consist.append(str(kendalltau(l1,l2)[0]))
#     fout.write('\t'.join(consist)+'\n')
# fout.close()


# MSnDCG@0003	NCUrb,P	Q@0003	P-measure	O-measure	NCUgu,BR	Q-measure	ERR	RR	Q@0005	AP@0005	AP@0003	P-plus	NCUrb,BR	Hit@0005	Hit@0003	nERR@0005	nERR@0003	nDCG@0005	NCUgu,P	nDCG@0003
metric_set = SM['0001'].keys()
# metric_list = list(metric_set)
metric_list = ['MSnDCG@0003',
               'P-measure',
               'ERR',
               'RR',
               'nERR@0005',
               'nERR@0003',
               'NCUrb,BR',
               'Nor-tbg-raw-step',
               'Nor-tbg-exp-step',
               'ERP']
metric_list.sort()

fout = open('../data/20161103.selected_consistency.tsv', 'w')
fout.write('dumb\t')
fout.write('\t'.join(metric_list) + '\n')
for i in range(0, len(metric_list), 1):
    consist = []
    consist.append(metric_list[i])
    for j in range(0, len(metric_list), 1):
        if j < i:
            consist.append('')
        else:
            m1 = metric_list[i]
            m2 = metric_list[j]

            topics = list(SM.keys())
            import numpy
            import math
            # l1 = [numpy.mean([run[t][m1] for t in topics]) for run in [BAIDU, SOGOU, SM, HAOSOU]]
            # l2 = [numpy.mean([run[t][m2] for t in topics]) for run in [BAIDU, SOGOU, SM, HAOSOU]]
            from scipy.stats import kendalltau

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

# how to define consistent:


# load query2id file
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

sbs_data = [item for item in contents if ((item[-3] != 'None') and (item[-3] != 'sogou') and (item[-3] != ''))]

# user preference:  (qid, source) = sbs
sbs_preference = dict()
details = defaultdict(lambda: ' ')
for item in sbs_data:
    query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments,_ = item
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
        if (A[queryid][m] < B[queryid][m] and int(sbs) < 0)  \
                or ( int(sbs) == 0  and abs(A[queryid][m] - B[queryid][m]) < 0.05 * max(abs(A[queryid][m]), abs(A[queryid][m])))\
                or ( A[queryid][m] > B[queryid][m] and int(sbs) > 0):
            consistent[m] += 1
            details[(queryid,source, m)] = 'CONSIST'
        else:
            inconsistent[m] += 1
            details[(queryid,source,m)] = ''
            if int(sbs) == 0:
                details[(queryid,source,m)] += 'P='
            elif int(sbs) > 0:
                details[(queryid,source,m)] += 'P>'
            else:
                details[(queryid,source, m)] +='P<'

            if (abs(A[queryid][m] - B[queryid][m]) < 0.05 * max(abs(A[queryid][m]), abs(B[queryid][m]))) or (A[queryid][m] == B[queryid][m]):
                details[(queryid,source,m)] +='M='
            else:
                if A[queryid][m] < B[queryid][m]:
                    details[(queryid, source, m)] += 'M<'
                elif  A[queryid][m] > B[queryid][m]:
                    details[(queryid,source, m)] += 'M>'

            if details[(queryid,source,m)] != 'CONSIST' and len(details[(queryid,source,m)] ) != 4:
                print source, queryid,A[queryid][m],m , B[queryid][m],sbs,details[(queryid,source,m)]

fout = open('../data/consistent_rate_metric.tsv', 'w')

for m in consistent:
    fout.write(m + '\t' + str(float(consistent[m])) + '\t' + str(float(inconsistent[m])) + '\n')
fout.close()


for compare in ['baidu','sm','haosou']:
    fout = open('../data/detail_metric_sbs.'+compare+'.tsv','w')
    queries = [query2id[item]+':'+item for item in query2id]
    queries.sort()

    fout.write('Metric\t'+'\t'.join(queries)+'\n')
    for m in metric_list:
        fout.write(m+'\t')
        queryids = [item.split(':')[0] for item in queries]
        fout.write('\t'.join([details[(q,compare,m)] for q in queryids]))
        fout.write('\n')
    fout.close()

