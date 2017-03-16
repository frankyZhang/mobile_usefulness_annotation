#coding=utf-8

__author__='luocheng'

import sys
sys.path.append('../../utils')
from LogUnit.ActionSeries import ActionSeries
from LogUnit.DataHub import DataHub
from LogUnit.LogParser import LogParser

dataHub = DataHub()
validUsers = dataHub.getValidId()



def extract_clicked_urls():
    allData = LogParser().getAllInteractionData()

    for user, config, interactions in allData:
        for t in interactions:
            for actionSeries in interactions:
                if actionSeries.postion == 'LP':
                    for action in actionSeries.actionSeries:
                        if action.actionName == 'CLICK_RESULT':
                            url = action

extract_clicked_urls()