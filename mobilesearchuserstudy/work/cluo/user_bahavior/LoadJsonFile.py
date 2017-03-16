#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json

sys.path.append('../../../utils')
from LogUnit.ActionSeries import ActionSeries
from LogUnit.DataHub import DataHub
from LogUnit.LogParser import LogParser



from collections import defaultdict

def mapUrl2TaskAndUrl():
    task2source2url2position = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:dict())))
    data = json.loads(open('../../../data/anno_url.json').read())
    fout = open('../../../data/anno_url.csv','w')
    for item in data:
        id = item['id']
        result_id = item['result_id']
        setting_id = item['setting_id']

        url = item['url']
        task_id = item['task_id']

        source_id = DataHub().getSource(int(setting_id), int(task_id))
        task2source2url2position[int(task_id)][source_id][url]= result_id
        fout.write('\t'.join([id,setting_id,task_id,url])+'\n')
    fout.close()

    def match(a, b):
        _max = -1
        if len(a) >= len(b):
            a,b = b,a
        for j in range(0, 1,1):
            i = 0
            while i+j < len(a) and i < len(b):
                if a[i+j] != b[i]:
                    break
                else:
                    i+=1
            _max = max(i, _max)
        return _max
    allData = LogParser().getAllInteractionData()

    fout = open('./data/clicked_url_2_rank.tsv','w')

    fout.write('task\tsource\trank\tclicked url\n')
    for item in allData:

        user = item[0]
        setting_id = DataHub().getId2Config()[str(user)]
        config = item[1]
        interactions = item[2]
        for t in interactions:
            source_id = DataHub().getSource(int(setting_id), int(t))

            # print user,config, t, interactions[t]

            for actionSeries in interactions[t]:
                if actionSeries.location == 'LP':
                    for action in actionSeries.actionSeries:
                        if action.actionName == 'CLICK_RESULT':
                            url = action.attributes['URL']
                            _max_sim = -1.0
                            _best_url = ''
                            for u in task2source2url2position[int(t)][source_id]:
                                if match(a=url, b = u) > _max_sim:
                                    _max_sim = match(a=url, b = u)
                                    _best_url = u
                            # if _max_sim < 100:
                            if True:
                                print url
                                print _best_url
                                print _max_sim
                                print '----'

                            result_id = task2source2url2position[int(t)][source_id][_best_url]
                            fout.write('\t'.join([str(t), str(source_id), str(result_id), str(url)]))
                            fout.write('\n')



    fout.close()



mapUrl2TaskAndUrl()

