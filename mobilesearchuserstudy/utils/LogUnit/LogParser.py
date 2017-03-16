#coding=utf8
__author__='luocheng'
from Action import Action
from ActionSeries import ActionSeries
from collections import defaultdict

class LogParser:
    def __init__(self):
        pass

    def parseLog(self,filename):
        print filename
        actions = defaultdict(lambda: [])
        for l in open(filename):
            act = Action()
            act.parseFromLine(l)

            if act.task:
                #  here should be a status machine, I will finish it tonight.
                if act.actionName ==  'TASK_BEGIN':
                    currentAS = ActionSeries()
                    currentAS.location = 'SERP'
                    currentAS.actionSeries.append(act)

                elif act.actionName=='BACK_TO_SERP':
                    currentAS.actionSeries.append(act)
                    actions[act.task].append(currentAS)

                    currentAS = ActionSeries()
                    currentAS.location = 'SERP'
                    currentAS.actionSeries.append(act)

                elif act.actionName=='CLICK_RESULT':
                    currentAS.actionSeries.append(act)
                    actions[act.task].append(currentAS)

                    currentAS = ActionSeries()
                    currentAS.clickedUrl = act.attributes['URL']
                    currentAS.location = 'LP'
                    currentAS.actionSeries.append(act)

                elif act.actionName=='FINISH':
                    currentAS.actionSeries.append(act)
                    actions[act.task].append(currentAS)
                    break
                elif act.actionName == 'TASK_FINISH':
                    currentAS.actionSeries.append(act)
                    actions[act.task].append(currentAS)

                elif act.actionName in ['LONGPRESS','SINGLETAPUP_IN_LP','SINGLETAPUP','YCHANGE','FLING_IN_LP','LONGPRESS_IN_LP','SCROLL_IN_LP','FLING','GLETAPUP', 'YCHANGE_IN_LP','SCROLL','JUMP_TO_PAGE']:
                    currentAS.actionSeries.append(act)

                else:
                    print 'uncached action', act.actionName

        return actions

    def getAllInteractionData(self):
        from DataHub import DataHub
        user2config = DataHub().getId2Config()

        interactions =  []
        for u in user2config.keys():
            f = '../../../data/mobile_logs/'+u+'_mobile_search/'+u+'.log'
            interactions.append((u, user2config[u], self.parseLog(f)))
        return interactions






if __name__=='__main__':
    lp = LogParser()
    actions  = lp.parseLog('../../data/mobile_logs/2013010932_mobile_search/2013010932.log')
    for t in actions:
        print type(actions[t])
        for _as in actions[t]:
            print isinstance(_as, ActionSeries)
            print t, _as.location, len(_as.actionSeries), '|'.join([item.actionName for item in _as.actionSeries])


