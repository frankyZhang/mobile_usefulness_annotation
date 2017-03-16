#coding=utf8

import sys
sys.path.append('../../../utils')
from LogUnit.ActionSeries import ActionSeries
from LogUnit.DataHub import DataHub
from LogUnit.LogParser import LogParser

def extract_dwell_movement():
    dataHub = DataHub()
    validUsers = dataHub.getValidId()


    dtime  = open('./data/dwelltime.txt','w')
    movemt = open('./data/movement.txt','w')
    for u in validUsers:
        f = '../../../data/mobile_logs/'+u+'_mobile_search/'+u+'.log'
        parser = LogParser()
        interactions = parser.parseLog(f)
        for t in interactions:
            output = []
            output.append(str(u))
            output.append(str(t))

            output2 = []
            output2.append(str(u))
            output2.append(str(t))


            for _as in interactions[t]:
                k = _as.location
                v = str(_as.getDuration())
                v2 = str(_as.getFurthestMovement())
                output.append(k+'='+v)
                output2.append(k+'='+v2)

            dtime.write('\t'.join(output)+'\n')
            movemt.write('\t'.join(output2)+'\n')
    dtime.close()

def draw_dwell_time_on_clicks():
    from collections import  defaultdict
    dwelltime  = defaultdict(lambda:[])
    for l in open('./data/dwelltime.txt'):
        segs = l.strip().split('\t')
        counter = 0
        for item in segs[2:]:
            k,v = item.split('=')
            if k =='LP':
                dwelltime[counter].append(float(v))
                counter +=1
    _max_clicks = max(dwelltime.keys())
    import numpy
    _mean  =[numpy.mean(dwelltime[i]) for i in range(1, _max_clicks+1, 1)]
    _std = [numpy.std(dwelltime[i]) for i in range(1, _max_clicks+1,1)]

    import numpy as np
    import matplotlib.pyplot as plt


    fig,ax = plt.subplots()
    all_data = [dwelltime[x]  for x in range(0, _max_clicks+1,1)]

    ax.boxplot( all_data)

    index = range(1,_max_clicks+2,1)
    labels = [str(item )+'('+str(len(dwelltime[item]))+')' for item in range(0, _max_clicks+1,1)]
    plt.xlabel('# in Click Seq (# samples)')
    plt.ylabel('Dwell time (seconds)')

    plt.xticks(index, labels)

    plt.show()


def draw_view_depth():
    from collections import  defaultdict
    viewdepth  = defaultdict(lambda:[])
    for l in open('./data/movement.txt'):
        segs = l.strip().split('\t')
        counter = 0
        for item in segs[2:]:
            k,v = item.split('=')
            if k =='LP':
                viewdepth[counter].append(max(0.0, float(v))+1210)
                counter +=1
    _max_clicks = max(viewdepth.keys())
    import numpy
    _mean  =[numpy.mean(viewdepth[i]) for i in range(1, _max_clicks+1, 1)]
    _std = [numpy.std(viewdepth[i]) for i in range(1, _max_clicks+1,1)]

    import numpy as np
    import matplotlib.pyplot as plt


    fig,ax = plt.subplots()
    all_data = [viewdepth[x]  for x in range(0, _max_clicks+1,1)]

    ax.boxplot( all_data)

    index = range(1,_max_clicks+2,1)
    for i in index[:-1]:
        print i, all_data[i]
    labels = [str(item )+'('+str(len(viewdepth[item]))+')' for item in range(0, _max_clicks+1,1)]
    plt.xlabel('# in Click Seq (# samples)')
    plt.ylabel('View Depth (pixels)')

    plt.xticks(index, labels)

    plt.show()


def analysis_movement_data():
    pass

def draw_average_view_speed():
    from collections import defaultdict
    dwelltime = defaultdict(lambda: [])
    for l in open('./data/dwelltime.txt'):
        segs = l.strip().split('\t')
        for item in segs[2:]:

            k, v = item.split('=')
            if k == 'LP':
                dwelltime[(segs[0], segs[1])].append(float(v))

    viewdepth = defaultdict(lambda:[])
    for l in open('./data/movement.txt'):
        segs = l.strip().split('\t')
        for item in segs[2:]:
            k, v = item.split('=')
            if k == 'LP':
                viewdepth[(segs[0],segs[1])].append(max(0.0, float(v)) + 1210)

    viewspeed = defaultdict(lambda:[])
    triple = []
    for k in dwelltime:
        for i in range(0, len(dwelltime[k]),1):
            if dwelltime[k][i] < 3 or viewdepth[k][i] <=1210:
                continue
            viewspeed[i].append( viewdepth[k][i]/dwelltime[k][i])
            triple.append([viewdepth[k][i],dwelltime[k][i],viewdepth[k][i]/dwelltime[k][i]])
    triple.sort(key=lambda x:x[2])
    print triple

    for k in viewspeed:
        print k, len(viewspeed[k]), max(viewspeed[k]), min(viewspeed[k])
    _max_clicks = max(viewspeed.keys())
    import numpy

    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    all_data = [viewspeed[x] for x in range(0, _max_clicks + 1, 1)]

    ax.boxplot(all_data)

    index = range(1, _max_clicks + 2, 1)
    labels = [str(item) + '(' + str(len(viewspeed[item])) + ')' for item in range(0, _max_clicks + 1, 1)]
    plt.xlabel('# in Click Seq (# samples)')
    plt.ylabel('View Speed (pixel/second)')

    plt.xticks(index, labels)

    plt.show()

def estimate_h_for_tbg():
    viewdepth = []
    for l in open('./data/movement.txt'):
        segs = l.strip().split('\t')
        current_max = -1.0

        for item in segs[2:]:
            k, v = item.split('=')
            if k == 'SERP':
                current_max = max(current_max, float(v) + 1210)
        viewdepth.append(current_max)
    viewdepth.sort()
    i = 0
    while i < len(viewdepth) and viewdepth[i]==1210.0:
        i+=1
    print viewdepth
    return viewdepth[430]
if __name__=="__main__":
    print estimate_h_for_tbg()