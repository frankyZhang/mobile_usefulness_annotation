import os
from utils import load_content,load_query2id
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def load_and_check_data():
    rtr = dict()
    for source in ['haosou','sm','baidu','sogou']:
        for f in os.listdir('../newdata/match/'+source):
            if '.txt' in f:
                qid = f.split('.')[0]
                matched_positions = dict()
                lines = open('../newdata/match/'+source+'/'+f)
                for l in lines:
                    segs = l.split('\t')
                    matched_idx = segs[1]
                    left = segs[2]
                    right = segs[3]
                    top = segs[4]
                    bottom = segs[5]
                    if matched_idx in '12345':
                        left = float(left)
                        right = float(right)
                        top = float(top)
                        bottom = float(bottom)
                        matched_positions[int(matched_idx)] = (left,right,top,bottom)
                    if len(matched_positions.keys())>=5:
                        break
                rtr[qid+'.'+source] = matched_positions
    fout = open('../newdata/position.tsv','w')
    for f in rtr.keys():
        for i in range(1,6,1):
            left,right,top,bottom = rtr[f][i]
            fout.write('\t'.join([str(item) for item in [f,i,left,right,top,bottom]])+'\n')
    fout.close()
    return rtr

def draw_decay_function():
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 1200)
    print x
    l1, = plt.plot(x, [decay_ndcg2(item) for item in x], '-', linewidth=1,color='r')
    l2, = plt.plot(x, [decay_linear_with_first_viewport(item) for item in x], '-', linewidth=1,color='b')
    l3, = plt.plot(x, [decay_linear_without_first_viewport(item) for item in x], '--', linewidth=1, color='k')
    l4, = plt.plot(x, [decay_tbg(item) for item in x], '-', linewidth=1, color = 'y')
    l5, = plt.plot(x, [decay_tbg_new(item) for item in x], '-', linewidth=1, color='g')
    labels = ("nDCG", 'Linear with reward to 1st vp', 'Linear without reward to 1st vp', 'TBG-like','TBG-IMPRO')
    legend = plt.legend(labels)
    plt.xlabel("Position (pixel)")
    plt.ylabel("Decay Value")
    dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off
    plt.show()

def decay_ndcg(i):
    import math
    return 1.0/math.log(i/200+1+1,10)

def decay_ndcg2(i):
    import math
    return 1.0/( 1.0 + math.log(i/200+1,10 ))
def decay_linear_without_first_viewport(i):
    if i > 1200:
        return 0.0
    else:
        return (-1.0) * (float(i)) / 1200.0 + 1
def decay_linear_with_first_viewport(i):
    if i <440:
        return 1.0
    elif i >= 1200:
        return 0.0
    else:
        return (-1.0)*(i-440)/760+1
def decay_tbg(i):
    import math
    r = math.e**( (-1.0)* float(i)/(220.0)* math.log(2,math.e))
    return r

def decay_tbg_new(i):
    import math
    r = math.e**( (-1.0)* float(i)/(2200.0)* math.log(2,math.e))
    return r

def gain_raw(r):
    return float(r)

def gain_exp(r):
    return 2.0**(float(r))


def normalized_metric(decayfunc, gainfunc, gain_dist, results):
    if len(results) != 5:
        print 'Error: not five results'
        return 0.0
    orig = []
    ideal = []
    for r in results:
        start, end, gain =r
        orig.append([start, end, gain])
        ideal.append([start, end, 5.0])
    return metric(decayfunc, gainfunc, gain_dist, orig)/metric(decayfunc, gainfunc, gain_dist, ideal)

def metric(decayfunc, gainfunc, gain_dist, results):
    if len(results)!=5:
        print 'Error: not five results'
        return 0.0
    else:
        init = results[0][0]
        for item in results:
            item[0] -= init
            item[1] -= init
        rtr = 0.0
        for item in results:
            start, end, gain = item
            gain_distribution = gain_dist(start, end)

            while len(gain_distribution) < int(end) - int(start):
                gain_distribution.append(0.0)
            for i in range(int(start), int(end), 1):

                rtr += decayfunc(i) * gainfunc(gain) * gain_distribution[i-int(start)]
        return rtr

def gain_dist_step( start, end):
    length = (end-start)
    head = length/5
    rtr = [0.0] * int(length)
    for i in range(int(head)):
        rtr[i] = 1.0/float(int(head))
    return rtr
def gain_dist_binominal(start, end):
    from scipy.stats import binom
    import numpy as np
    rtr = binom.pmf(np.arange(0,end-start), 10, 0.3)
    return rtr



def calculate_erp():
    positions=  load_and_check_data()
    q2id = load_query2id()
    content = load_content()
    qid_source_rank_2_gain = dict()
    ready = dict()
    for l in content:

        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments, pr = l
        print len(l), score, pr
        qid = q2id[query]
        qid_source_rank_2_gain[qid+'.'+source+'.'+rank] = [float(score), float(pr)]

    for p in positions:
        ready[p] = []
        for i in range(1,6,1):
            # top, bottom, score, pr
            ready[p].append([positions[p][i][2], positions[p][i][3], qid_source_rank_2_gain[p + '.' + str(i)][0],  qid_source_rank_2_gain[p + '.' + str(i)][0] ])
    fout = open('../newdata/metrics.tsv','a')

    for p in ready:
        _erp = ERP(ready[p])
        fout.write('ERP\t'+p+'\t'+str(_erp)+'\n')
    fout.close()


def ERP(serp):
    erp = 0.0
    dissat = 1.0
    init = serp[0][0]
    for item in serp:
        top,bottom, score, killer = item
        if killer == 1:
            pr = 1.0
        else:
            pr = (2.0**score-1.0)/32.0
        print dissat, pr, decay_tbg(bottom-init)
        erp += dissat * pr * decay_tbg(bottom-init)
        if killer == 1:
            break
        dissat *= (1.0-pr)
    return erp


def calculate_metrics():
    positions = load_and_check_data()
    q2id = load_query2id()
    content = load_content()
    ready = dict()
    qidandsourceandrank2gain = dict()
    for l in content:
        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments,_ = l
        qid = q2id[query]

        qidandsourceandrank2gain[qid+'.'+source+'.'+rank] = float(score)

    for p in positions:
        ready[p] = []
        for i in range(1,6,1):
            ready[p].append([ positions[p][i][2],positions[p][i][3], qidandsourceandrank2gain[p+'.'+str(i)]])
    functions = [ normalized_metric]
    decay_func= [decay_ndcg2, decay_linear_with_first_viewport, decay_linear_without_first_viewport, decay_tbg]
    gain_func = [gain_raw,gain_exp]
    gain_dist_func = [gain_dist_step, gain_dist_binominal]
    fout = open('../newdata/metrics.tsv','w')
    for f in functions:
        for d in decay_func:
            for g in gain_func:
                for gd in gain_dist_func:
                    for p in ready:
                        fname,dname,gname, gdname = '','','',''
                        if 'normal' in f.__name__:
                            fname = 'Nor'
                        else:
                            fname = 'non'

                        if d.__name__ == 'decay_ndcg2':
                            dname = 'nDCG'
                        elif d.__name__=='decay_linear_with_first_viewport':
                            dname = 'lwfv'
                        elif d.__name__=='decay_linear_without_first_viewport':
                            dname = 'lwofv'
                        else:
                            dname = 'tbg'

                        if g.__name__ == 'gain_raw':
                            gname = 'raw'
                        else:
                            gname = 'exp'

                        if gd.__name__== 'gain_dist_step':
                            gdname = 'step'
                        else:
                            gdname = 'binom'
                        mname = '-'.join([fname,dname,gname, gdname])
                        mvalue = f(d,g,gd,ready[p])

                        fout.write('\t'.join([mname, p, str(mvalue)])+'\n')
    fout.close()








if __name__=='__main__':
    # print gain_dist_binominal(0,100)
    draw_decay_function()
    # calculate_metrics()
    # calculate_erp()
