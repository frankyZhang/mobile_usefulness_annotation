#coding=utf8
__author__ = 'luocheng'
__date__ = '21/12/2016-2:01 PM'


# 这部分分析主要解决这么一个问题: 1. 用户在landing page上的访问长度是什么样的； 建立一个什么样的model

import sys
sys.path.append('../../../utils')
from LogUnit.ActionSeries import ActionSeries
from LogUnit.DataHub import DataHub
from LogUnit.LogParser import LogParser



def getFineRelevance():
    relevance = []
    fout  =open('./data/fineRelevance.tsv','w')
    fout.write('taskid\tsource\tresultid\trelevance\n')
    for l in open('../../../data/anno_relevance.csv').readlines()[1:]:
        setting_id, task_id, result_id, relevance = l.strip().split(',')
        setting_id = int(setting_id)
        task_id = int(task_id)
        result_id = int(result_id)
        relevance = float(relevance)
        source = DataHub().getSource(setting_id, task_id)
        fout.write('\t'.join([str(task_id), str(source), str(result_id), str(relevance)]))
        fout.write('\n')
    fout.close()

def getFineNecessity():
    fout = open('./data/fineNecessity.tsv','w')
    fout.write('taskid\tsource\tresultid\tnecessity\n')
    for l in open('../../../data/anno_necessity.csv').readlines()[1:]:
        _, user_id, setting_id, task_id, result_id, score, results_number = l.strip().split('\t')
        setting_id = int(setting_id)
        task_id = int(task_id)
        result_id = int(result_id)
        necessity = int(score)
        source = DataHub().getSource(setting_id, task_id)
        fout.write('\t'.join([str(task_id), str(source), str(result_id), str(necessity)]))
        fout.write('\n')
    fout.close()


def extractClickedUrlDetails():
    url2rank = dict()
    for l in open('./data/clicked_url_2_rank.tsv').readlines()[1:]:
        task,source,rank,url = l.strip().split('\t')
        task = int(task)
        if rank == '':
            rank = 0
        else:
            rank = int(rank)
        url2rank[(task,source,url)] = rank
    allData = LogParser().getAllInteractionData()
    leavePos = []
    for item in allData:
        uid =item[0]
        settingid = item[1]
        interactions = item[2]
        for tid in interactions:
            source = DataHub().getSource(int(settingid), int(tid))
            leavePos.append( (uid, settingid,tid, getViewedLength(interactions[tid])))
            for _as  in interactions[tid]:
                if _as.location == 'SERP':
                    continue
                if _as.location == 'LP':
                    clickedUrl = _as.getClickedUrl()
                    rank = url2rank[(int(tid), source, clickedUrl)]
    leavePos.sort(key=lambda x: x[3])
    fout = open('./data/leave_position.tsv','w')
    fout.write('uid\tsettingid\ttid\tl\tratio\n')
    i = 0
    for leave in leavePos:
        uid, settingid, tid, l  = leave
        ratio = float(len(leavePos)- i)/float(len(leavePos))

        fout.write('\t'.join([str(item) for item in [uid, settingid,tid,l, ratio]]))
        fout.write('\n')
        i+=1
    fout.close()


def pk_hcs(_lambda,_miu, K):
    import math
    return (_lambda/2.0/math.pi/K**3)**0.5* math.exp(((-1.0)*(K-_miu)**2)/(2*(_miu)**2*K))

def pk_hcs_leave_possibility(_lambda, _miu, K):
    from scipy.stats import norm
    import math
    # https: // en.wikipedia.org / wiki / Inverse_Gaussian_distribution
    first = (_lambda/K)**0.5 * (K/_miu - 1.0)
    second = 2.0* _lambda/_miu
    third = (-1.0) * (_lambda/K)**0.5 * (K/_miu + 1.0)
    cdf =  norm.cdf(first)+ math.exp(second)* norm.cdf(third)
    return 1-cdf






def draw_norm_cdf():
    from scipy.stats import norm
    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots(1, 1)
    x = np.linspace(-3,3,1000)
    print norm.cdf(0.5)
    ax.plot(x, norm.cdf(x))
    plt.show()


def fitting_hcs():
    import math
    samplepoints = []
    for l in open('./data/leave_position.tsv').readlines()[1:]:
        segs = l.strip().split('\t')
        ratio = float(segs[-1])
        l = float(segs[-2])
        samplepoints.append((l, ratio))

    best_cha  = 2**32
    best_lambda = None
    best_miu = None
    for _lambda in range(23070, 23080, 1):
        print _lambda
        for _miu in range(13300,13600,10):
            _cha = 0.0
            for s in samplepoints:
                position, ratio = s
                _cha += abs(ratio - pk_hcs_leave_possibility(_lambda, _miu, position))
            if _cha < best_cha:
                best_cha, best_lambda, best_miu = _cha, _lambda, _miu
    print best_cha, best_lambda, best_miu

    # res = 5.56690457015
    # lambda = 23070
    # miu = 13510



def draw_pk_hcs_leave_possibility():
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(1, 80000, 10000)
    y = [pk_hcs_leave_possibility(10000, 10000, item) for item in x]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y)

    plt.show()


def fittingDecayFunc(parah = None):
    import math
    samplepoints = []
    for l in open('./data/leave_position.tsv').readlines()[1:]:
        segs = l.strip().split('\t')
        ratio = float(segs[-1])
        l = float(segs[-2])
        samplepoints.append((l,ratio))

    if parah == None:
        best_dist = 2**64
        best_h = None
        h = 10000.0
        while h < 11000.0:
            print h
            _d = 0
            for l, ratio in samplepoints:
                predict_ratio  = math.e**((-1.0)*math.log(2)* l / float(h))
                _d += abs(predict_ratio-ratio)
            if _d < best_dist:
                best_dist = _d
                best_h = h
            h += 0.01


        # best_h = 10069.13
        # best_dist = 63.08
        print best_h, best_dist
        parah=best_h

        return

    # 10630.43
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.linspace(0,80000, 10000)
    y = [math.e**((-1.0)*math.log(2)* item / 10069.13 ) for item in x]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    sx = [item[0] for item in samplepoints]
    sy = [item[1] for item in samplepoints]

    hx = np.linspace(1,80000, 10000)
    hy = [pk_hcs_leave_possibility(23070,13510, item  ) for item in hx]
    plt.xlim(0,80000)
    plt.ylim(0,1)



    exp = ax.plot(x, y, color='b', label='Exponential decay', linestyle='--' , linewidth=2.0)
    # ax.plot(sx,sy)
    igd = ax.plot(hx, hy, color='r', label='Inverse Gaussian decay',linewidth=2.0)

    point = plt.scatter(sx, sy,color='g',s=24.45, alpha=0.15, label='Users')

    ax.set_xlabel('Height (pixels)', fontsize=16)
    ax.set_ylabel('D(h)', fontsize=16)
    plt.tight_layout()
    plt.legend()

    plt.show()







def getViewedLength(asList):
    length  = []
    for _as in asList:
        length.append((_as.location, _as.getFurthestMovement()))
    s = 0
    maxserp = -1
    for i in length:
        location, l = i
        if location =='SERP':
            maxserp = max(maxserp, l)
        elif location =='LP':
            s += l+1060
    s += maxserp+1060
    return s



def getClickedRelevanceList():
    urlset = set()
    for l in open('./data/clicked_url_2_rank.tsv').readlines()[1:]:
        task, source, rank, url = l.strip().split('\t')
        urlset.add(url)
    idx = 1
    listcontent = []
    fout = open('./index.html.urllist.txt','w')
    for u in urlset:
        fout.write(str(idx) +'\t'+ u+'\n')
        _c  = '<li><a href="'+u+'">'+str(idx)+'</a></li>'
        idx +=1
        listcontent.append(_c)
    fout.close()

    listcontent = '\n'.join(listcontent)
    open('./data/index.html','w').write( open('./data/index.html.template').read().replace('{{listcontent}}', listcontent))



def estimatePClickGivenRel():

    url2rank = dict()
    for l in open('./data/clicked_url_2_rank.tsv').readlines()[1:]:
        task, source, rank, url = l.strip().split('\t')
        task = int(task)
        if rank == '':
            rank = 0
        else:
            rank = int(rank)
        url2rank[(task, source, url)] = rank

    from collections import defaultdict
    presentation = defaultdict(lambda:0)
    click = defaultdict(lambda:0)


    allData = LogParser().getAllInteractionData()
    for item in allData:

        uid = item[0]
        settingid = item[1]
        interactions = item[2]
        for tid in interactions:
            source = DataHub().getSource(int(settingid), int(tid))
            clicked = []
            for _as in interactions[tid]:
                if _as.location == 'SERP':
                    continue
                if _as.location == 'LP':
                    clickedUrl = _as.getClickedUrl()
                    rank = url2rank[(int(tid), source, clickedUrl)]
                    clicked.append(int(rank))

            if clicked:
                furthest_click  = max(clicked)
                for i in range(0, furthest_click+1, 1):
                    presentation[(int(tid), source, int(i))]+=1

                for r in clicked:
                    click[(int(tid), source, r)]+=1

    # load tid, source, r, to relevance;
    relevance = dict()
    for l in open('./data/fineRelevance.tsv').readlines()[1:]:
        taskid,source,resultid,rel = l.strip().split('\t')
        taskid = int(taskid)
        resultid = int(resultid)
        rel = int(float(rel))
        relevance[(taskid, source, resultid)] = rel

    pre_by_rel = defaultdict(lambda: 0)
    click_by_rel = defaultdict(lambda: 0)
    print relevance.keys()
    for k in presentation:
        result_relevance = relevance[k]
        pre_by_rel[result_relevance] += presentation[k]
        click_by_rel[result_relevance] += click[k]

    for v in pre_by_rel:
        print 'Rel', v, float(click_by_rel[v])/float(pre_by_rel[v])

    # Rel 1    0.281188118812
    # Rel 2    0.356302521008
    # Rel 3    0.458479532164
    # Rel 4    0.734702992407


def estimatePClickGivenRelandNeces():
    url2rank = dict()
    for l in open('./data/clicked_url_2_rank.tsv').readlines()[1:]:
        task, source, rank, url = l.strip().split('\t')
        task = int(task)
        if rank == '':
            rank = 0
        else:
            rank = int(rank)
        url2rank[(task, source, url)] = rank

    from collections import defaultdict
    presentation = defaultdict(lambda: 0)
    click = defaultdict(lambda: 0)

    allData = LogParser().getAllInteractionData()
    for item in allData:

        uid = item[0]
        settingid = item[1]
        interactions = item[2]
        for tid in interactions:
            source = DataHub().getSource(int(settingid), int(tid))
            clicked = []
            for _as in interactions[tid]:
                if _as.location == 'SERP':
                    continue
                if _as.location == 'LP':
                    clickedUrl = _as.getClickedUrl()
                    rank = url2rank[(int(tid), source, clickedUrl)]
                    clicked.append(int(rank))

            if clicked:
                furthest_click = max(clicked)
                for i in range(0, furthest_click + 1, 1):
                    presentation[(int(tid), source, int(i))] += 1

                for r in clicked:
                    click[(int(tid), source, r)] += 1

    # load tid, source, r, to relevance;
    relevance = dict()
    for l in open('./data/fineRelevance.tsv').readlines()[1:]:
        taskid, source, resultid, rel = l.strip().split('\t')
        taskid = int(taskid)
        resultid = int(resultid)
        rel = int(float(rel))
        relevance[(taskid, source, resultid)] = rel

    necessity = dict()
    for l in open('./data/fineNecessity.tsv').readlines()[1:]:
        taskid, source, resultid, rel = l.strip().split('\t')
        taskid = int(taskid)
        resultid = int(resultid)
        nec = int(float(rel))
        necessity[(taskid, source, resultid)] = nec

    pre_by_rel = defaultdict(lambda: 0)
    click_by_rel = defaultdict(lambda: 0)
    print relevance.keys()
    for k in presentation:
        result_relevance = relevance[k]
        result_necessity = necessity[k]
        pre_by_rel[(result_relevance, result_necessity)] += presentation[k]
        click_by_rel[(result_relevance, result_necessity)] += click[k]

    for r in range(1, 5,1):
        print [float(click_by_rel[(r, v)]) / float(pre_by_rel[(r,v)]) for v in [1,2,3]]

    countofresults = defaultdict(lambda:0)
    for item in relevance:
        rel = relevance[item]
        nec = necessity[item]
        countofresults[(rel, nec)]+=1
    for k in countofresults:
        print k, countofresults[k]


if __name__=='__main__':
    estimatePClickGivenRelandNeces()
    # fittingDecayFunc(10069.13)
    # estimatePClickGivenRel()
    # draw_pk_hcs()
    # fittingDecayFunc(10069.13)
    # draw_pk_hcs_leave_possibility()
    # fitting_hcs()
    fittingDecayFunc(10069.13)
    # estimatePClickGivenRelandNeces()