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
# load query2id file
query2id = dict()
for l in open('../data/query.idx'):
    segs = l.strip().split('\t')
    query, id = segs
    query2id[query] = id

from collections import defaultdict


metric_set = SM['0001'].keys()
metric_list = list(metric_set)

sbs_data = [item for item in contents if ((item[-3] != 'None') and (item[-3] != 'sogou') and (item[-3] != ''))]


# user preference:  (qid, source) = sbs

# option = 'ABS' or 'REL';
# ratio  = value
def err_change_with_relative_ratio(ratio, option):
    consistent = defaultdict(lambda: 0)
    inconsistent = defaultdict(lambda: 0)

    sbs_preference = dict()
    sbs_comments_global = dict()
    details = defaultdict(lambda: ' ')
    for item in sbs_data:
        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments, _ = item
        queryid = query2id[query]
        print query, queryid

        A = SOGOU
        if source == 'baidu':
            B = BAIDU
        elif source == 'sm':
            B = SM
        elif source == 'haosou':
            B = HAOSOU

        if '-' in sbs or sbs.isdigit():
            sbs_preference[(queryid, source)] = int(sbs)
            sbs_comments_global[(queryid, source)] = str(sbs_comments)
        for m in metric_list:

            equal = None
            if option == 'REL':
                equal = (int(sbs) == 0 and abs(A[queryid][m] - B[queryid][m]) <= ratio * max(abs(A[queryid][m]),B[queryid][m]))
            elif option == 'ABS':
                equal = (int(sbs) == 0 and abs(A[queryid][m] - B[queryid][m]) <= ratio)

            if (A[queryid][m] < B[queryid][m] and int(sbs) < 0) \
                    or (A[queryid][m] > B[queryid][m] and int(sbs) > 0) \
                    or equal == True:
                consistent[m] += 1
                details[(queryid, source, m)] = 'CONSIST'
            else:
                inconsistent[m] += 1
                details[(queryid, source, m)] = ''
                if int(sbs) == 0:
                    details[(queryid, source, m)] += 'P='
                elif int(sbs) > 0:
                    details[(queryid, source, m)] += 'P>'
                else:
                    details[(queryid, source, m)] += 'P<'


                if A[queryid][m] < B[queryid][m]:
                    details[(queryid, source, m)] += 'M<'
                elif A[queryid][m] > B[queryid][m]:
                    details[(queryid, source, m)] += 'M>'
                else:
                    details[(queryid, source, m)] += 'M='
                    # print equal, A[queryid][m], B[queryid][m]

                if details[(queryid, source, m)] != 'CONSIST' and len(details[(queryid, source, m)]) != 4:
                    print source, queryid, A[queryid][m], m, B[queryid][m], sbs, details[(queryid, source, m)]

    fout = open('../result/consistent_rate_metric/'+option+'_'+str(ratio)+'.tsv', 'w')

    for m in consistent:
        fout.write(m + '\t' + str(float(consistent[m])) + '\t' + str(float(inconsistent[m])) + '\n')
    fout.close()

    for compare in ['baidu', 'sm', 'haosou']:
        fout = open('../result/err/err_detail_metric_sbs/'+option+'.'+str(ratio)+'.' + compare + '.tsv', 'w')
        queries = [query2id[item] + ':' + item for item in query2id]
        queries.sort()

        fout.write('Metric\t' + '\t'.join(queries) + '\n')
        for m in metric_list:
            fout.write(m + '\t')
            queryids = [item.split(':')[0] for item in queries]
            fout.write('\t'.join([details[(q, compare, m)] for q in queryids]))
            fout.write('\n')
        fout.close()

    fout = open('../result/err/ERR_detail/'+option+'.'+str(ratio)+'.tsv', 'w')
    fout.write(
        'Target System\tQuery\tConsistent\tSogou Relevance\tTarget System Relevance\tSBS\tSBS Comments\tERR Sogou\tERR Target System\tSogou Page\tTarget Page\n')
    for compare in ['baidu', 'sm', 'haosou']:

        queries = [query2id[item] + ':' + item for item in query2id]
        queries.sort()

        for q in queries:
            qid, qcontent = q.split(':')
            m = 'ERR'
            if details[(qid, compare, m)] != 'CONSIST':
                output = []
                output.append(compare)
                output.append(q)
                output.append(details[(qid, compare, m)])
                # get sogou relevance
                sogoudata = [item[6] for item in contents if item[0] == qcontent and item[1] == 'sogou']
                output.append('|'.join(sogoudata))
                # get target relevance
                targetdata = [item[6] for item in contents if item[0] == qcontent and item[1] == compare]

                output.append('|'.join(targetdata))
                output.append(sbs_preference[(qid, compare)])
                output.append(sbs_comments_global[(qid, compare)])
                A = SOGOU
                if compare == 'baidu':
                    B = BAIDU
                elif compare == 'sm':
                    B = SM
                elif compare == 'haosou':
                    B = HAOSOU
                output.append(A[qid]['ERR'])
                output.append(B[qid]['ERR'])

                fout.write('\t'.join([str(item) for item in output]))
                fout.write('\n')
    fout.close()


def analysis_err():
    r = 0.01
    while r < 0.31:
        err_change_with_relative_ratio( r,'ABS')
        err_change_with_relative_ratio( r,'REL')
        r +=0.01


# analysis_err()

def intergrate_err():
    from collections import defaultdict
    import os

    absolute = defaultdict(lambda:defaultdict(lambda:None))
    relative = defaultdict(lambda:defaultdict(lambda:None))
    for f in os.listdir('../result/consistent_rate_metric'):
        if '.tsv' in f:
            tag = f[0:3]
            r = f.split('_')[1].replace('.tsv','')
            print r
            for l in open('../result/consistent_rate_metric/'+f):
                m,ag,disag = l.strip().split('\t')
                if tag  == 'ABS':
                    absolute[m][r] = float(ag)/150.0
                elif tag == 'REL':
                    relative[m][r] = float(ag)/150.0

    abs_out = open('../result/absolute.tsv','w')
    rel_out = open('../result/relative.tsv','w')

    all_out = open('../result/various_thresold','w')
    for m in ['ERR','RR','nERR@0005', 'ERP', 'AP@0003', 'nDCG@0003','Nor-tbg-raw-step']:
        abs_content = [m+'-ABS']
        rel_content = [m+'-REL']

        r = 0.01
        while r < 0.31:
            abs_content.append(absolute[m][str(r)])
            rel_content.append(relative[m][str(r)])
            print r
            r += 0.01
        abs_out.write('\t'.join([str(item) for item in abs_content])+'\n')
        rel_out.write('\t'.join([str(item) for item in rel_content]) + '\n')
        all_out.write('\t'.join([str(item) for item in abs_content])+'\n')
        all_out.write('\t'.join([str(item) for item in rel_content]) + '\n')
    abs_out.close()
    rel_out.close()
    all_out.close()


# intergrate_err()


def predict_sbs_performance(ratio,option, tiebreak):
    consistent = defaultdict(lambda: 0)
    inconsistent = defaultdict(lambda: 0)

    sbs_preference = dict()
    sbs_comments_global = dict()
    details = defaultdict(lambda: ' ')
    for item in sbs_data:
        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments, _ = item
        queryid = query2id[query]
        print query, queryid

        A = SOGOU
        if source == 'baidu':
            B = BAIDU
        elif source == 'sm':
            B = SM
        elif source == 'haosou':
            B = HAOSOU

        if '-' in sbs or sbs.isdigit():
            sbs_preference[(queryid, source)] = int(sbs)
            sbs_comments_global[(queryid, source)] = str(sbs_comments)
        for m in metric_list:
            threshold = None
            if option == 'REL':
                threshold =  ratio * max(abs(A[queryid][m]),B[queryid][m])
            elif option == 'ABS':
                threshold = ratio
            if abs(A[queryid][m] - B[queryid][m]) < threshold:
                if tiebreak == 'HARD':
                    predict_sbs =  0
                elif tiebreak=='SOFT':
                    continue

            elif A[queryid][m] < B[queryid][m] :
                predict_sbs =-1
            elif A[queryid][m] > B[queryid][m] :
                predict_sbs = 1

            if (predict_sbs < 0 and int(sbs) <0) or (predict_sbs > 0 and int(sbs) >0) or (predict_sbs == 0 and int(sbs) ==0):

                consistent[m] +=1
            else:
                inconsistent[m] +=1
    fout = open('../result/predict_sbs/PRED.'+option+'.'+str(ratio)+'.'+tiebreak+'.tsv','w')
    for m in consistent:
        fout.write(m + '\t' + str(float(consistent[m])) + '\t' + str(float(inconsistent[m])) + '\n')
    fout.close()


def predict_sbs_batch():
    t = 0.01
    while t < 0.31:
        predict_sbs_performance(t, 'ABS','HARD')
        predict_sbs_performance(t, 'ABS', 'SOFT')
        predict_sbs_performance(t, 'REL','HARD')
        predict_sbs_performance(t, 'REL', 'SOFT')

        t+=0.01


def intergrate_predict_err(tiebreak):
    from collections import defaultdict
    import os

    absolute = defaultdict(lambda:defaultdict(lambda:None))
    relative = defaultdict(lambda:defaultdict(lambda:None))
    for f in os.listdir('../result/predict_sbs'):
        if '.tsv' in f and tiebreak in f:
            tag = f.split('.')[1]
            r = f.replace('PRED.ABS.','').replace("PRED.REL.",'').replace('.HARD.tsv','').replace('.SOFT.tsv','')
            print r
            for l in open('../result/predict_sbs/'+f):
                m,ag,disag = l.strip().split('\t')
                if tag  == 'ABS':
                    absolute[m][r] = float(ag)/(float(ag)+float(disag))
                elif tag == 'REL':
                    relative[m][r] = float(ag)/(float(ag)+float(disag))
    print absolute,relative
    abs_out = open('../result/predict.sbs.abs.'+tiebreak+'.tsv','w')
    rel_out = open('../result/predict.sbs.rel.'+tiebreak+'.tsv','w')

    all_out = open('../result/predict.sbs.all.'+tiebreak+'.tsv','w')
    for m in ['ERR', 'ERP', 'AP@0003', 'nDCG@0003','Nor-tbg-raw-step']:
        abs_content = [m+'-ABS']
        rel_content = [m+'-REL']

        r = 0.01
        while r < 0.31:
            abs_content.append(absolute[m][str(r)])
            rel_content.append(relative[m][str(r)])
            print r
            r += 0.01
        abs_out.write('\t'.join([str(item) for item in abs_content])+'\n')
        rel_out.write('\t'.join([str(item) for item in rel_content]) + '\n')
        all_out.write('\t'.join([str(item) for item in abs_content])+'\n')
        all_out.write('\t'.join([str(item) for item in rel_content]) + '\n')
    abs_out.close()
    rel_out.close()
    all_out.close()

# predict_sbs_batch()
intergrate_predict_err('HARD')
intergrate_predict_err('SOFT')
# intergrate_err()

