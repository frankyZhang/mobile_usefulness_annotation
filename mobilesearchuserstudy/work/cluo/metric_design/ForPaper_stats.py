#coding=utf8
__author__ = 'luocheng'
__date__ = '18/01/2017-2:03 AM'



def count_results():
    import numpy
    from collections import defaultdict
    count = defaultdict(lambda:0)
    for l in open('../../../data/anno_relevance.csv').readlines()[1:]:
        s,t,r,relevance = l.split(',')
        count[(s,t)]+=1


    numbers = [ count[item] for item in count.keys()]
    print numpy.mean(numbers), numpy.std(numbers)


def count_clicks():
    import sys
    sys.path.append('../../../utils')
    from LogUnit.ActionSeries import ActionSeries
    from LogUnit.DataHub import DataHub
    from LogUnit.LogParser import LogParser
    dataHub = DataHub()


if __name__=='__main__':
    count_results()