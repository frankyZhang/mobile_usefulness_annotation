#coding=utf8
__author__='luocheng'

class ActionSeries:
    def __init__(self):
        self.location = None
        self.type = None
        self.clickedUrl = None
        self.actionSeries = []

    """
    2016年11月22日和张帆逻辑
    主要需要压缩的是几个元组，FLYING和SCROLL即，改变了viewport的行为；
        有没有什么限制，

    """


    def getDuration(self):
        if len(self.actionSeries) <=1:
            return -1
        else:
            start = self.actionSeries[0]
            end = self.actionSeries[-1]
            return (end.timeStamp - start.timeStamp)/1000.0

    def getFurthestMovement(self):
        ymax = -1
        for item in self.actionSeries:
            if 'Y' in item.attributes:
                ymax = max(ymax, float(item.attributes['Y']))
        return ymax

    def getContentLength(self):
        length = -1


    def getLocation(self):
        return self.location

    def getClickedUrl(self):
        if self.getLocation() == 'SERP':
            return None
        elif self.getLocation()=='LP':
            return self.clickedUrl

    def compress(self):
        _temp = []
        for act in self.actionSeries:
            pass
        pass
    def getSpecificTypeOfActions(self, _type):
        return [item for item in self.actionSeries if item.actionName == _type]



