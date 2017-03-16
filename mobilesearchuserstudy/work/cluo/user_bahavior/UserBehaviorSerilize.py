#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('../../../utils')
from LogUnit.DataHub import DataHub
from LogUnit.LogParser import LogParser

def test():
    dh = DataHub()
    print dh.getValidId()

def serilize():

    url2rank = dict()
    for l in open('./data/clicked_url_2_rank.tsv').readlines()[1:]:
        task,source,rank,url = l.strip().split('\t')
        task = int(task)
        if rank == '':
            rank = 0
        else:
            rank = int(rank)
        url2rank[(task,source,url)] = rank

    fout = open('./data/temp_abstract_interaction.tsv','w')


    allData = LogParser().getAllInteractionData()
    for item in allData:
        uid = item[0]
        configid = item[1]
        interactions= item[2]
        for tid in interactions:

            source = DataHub().getSource(int(configid), int(tid))

            fout.write('BEGIN\t'+str(uid)+'\t'+str(configid)+'\t'+source+'\t'+str(tid)+'\n')
            for _as in interactions[tid]:
                if _as.location=='SERP':
                    fout.write('SERP\t'+str(_as.getDuration())+'\n')
                if _as.location =='LP':
                    clickedUrl = _as.getClickedUrl()
                    rank = url2rank[(int(tid), source, clickedUrl )]
                    fout.write('LP\t'+str(_as.getDuration())+'\t'+str(rank)+'\n')
            fout.write('END\n')

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
import numpy as np
def drawOne(data,title):
    #session: source,user,[(serp,duration), (lp, duration, rank)]

    print len(data)
    numOfSubplots = len(data)
    fig = figure()
    fig.set_size_inches(10.5, 18.5)
    tt = title.split('_')[0] +'_'+title.split('_')[1]
    plt.title(tt)




    session_idx = 0
    axoverall =None
    for session in data:
        if session_idx == 0:
            ax = fig.add_subplot(numOfSubplots,1, 1)
            axoverall = ax
            session_idx+=1
        else:
            ax = fig.add_subplot(numOfSubplots,1, session_idx+1, sharex =axoverall)
            session_idx+=1

        ax.set_ylim(0,10)
        ax.set_xlim(0,300)

        source = session[0]
        user = session[1]
        ax.set_ylabel(user)

        if source == 'sogou':
            _color = 'orange'
        elif source == 'baidu':
            _color='blue'
        elif source == 'haosou':
            _color ='green'
        elif source =='sm':
            _color = 'purple'

        cummX = 0
        for item in session[2]:
            print item
            if item[0] == 'SERP':
                _duration  = float(item[1])
                _x = np.linspace(cummX, cummX+_duration)
                _y = [0.0] *  len(_x)
                ax.plot(_x, _y ,'-',linewidth=6, color =_color)
                cummX+= _duration
            elif item[0] == 'LP':
                _duration = float(item[1])
                _rank = float(item[2])
                _x = np.linspace(cummX, cummX+_duration)
                _y = [_rank+1.0] *  len(_x)
                ax.plot(_x, _y ,':',linewidth=6, color =_color)

                cummX+= _duration
        ax.grid(True)
    plt.xticks([])
    # plt.show()
    # fig.set_size_inches(10.5, 18.5)
    plt.savefig('./figu/'+tt+'.png')
    plt.close()

def draw():
    dh = DataHub()
    from collections import defaultdict
    data = defaultdict(lambda:[])

    temp = []
    for l in open('./data/temp_abstract_interaction.tsv'):
        if l.strip()!= 'END':
            temp.append(l.strip())
        else:
            _, uid, configid, source,tid =temp[0].split('\t')
            segs = [ item.split('\t') for item in temp[1:]]
            data[(tid, source)].append((source,uid, segs))
            temp = []
    for k in data:
        tid, source = k
        filename = tid+'_'+source+'_'+dh.id2query(int(tid))
        print data[k]
        drawOne(data[k], filename)
        print data[k]


def mergePictures():
    import sys
    from PIL import Image
    for i in range(1,21,1):
        images = map(Image.open,  [ './figu/'+ str(i)+ item for item in ['_sogou.png','_haosou.png','_sm.png', '_baidu.png']])
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]

        new_im.save('./figu/'+str(i)+'.png')


if __name__ =='__main__':
    draw()
    mergePictures()