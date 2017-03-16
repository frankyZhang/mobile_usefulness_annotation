#coding=utf8
__author__ = 'luocheng'
__date__ = '18/01/2017-5:15 PM'


from collections import defaultdict
count = defaultdict(lambda:0)
for l in open('./data/dwelltime.txt'):
    segs = l.strip().split('\t')
    user, task = segs[0], segs[1]
    count[(user, task)]=0
    for s in segs[2:]:
        source, time = s.split('=')
        if source=='LP':
            count[(user,task)] +=1
vector = [count[item] for item in count]
import numpy

print sum(vector), numpy.mean(vector), numpy.std(vector), max(vector),min(vector)
