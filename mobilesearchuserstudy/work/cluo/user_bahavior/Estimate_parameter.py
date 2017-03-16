import struct
import imghdr
import sys
sys.path.append('../../../utils')
from LogUnit.ActionSeries import ActionSeries
from LogUnit.DataHub import DataHub
from LogUnit.LogParser import LogParser

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

import os

path = '/Users/luocheng/Documents/coderepo/mobilesearch/metric_design/data/serp_screenshots'

height = [get_image_size(path+'/'+f)[1] for f in os.listdir(path) if 'png' in f]
import numpy as np
print np.mean(height) #2553.77
allData = LogParser().getAllInteractionData()
contentheight = []
for item in allData:
    user = item[0]
    config = item[1]
    interactions = item[2]
    for t in interactions:
        # print user,config, t, interactions[t]
        for actionSeries in interactions[t]:
            for action in actionSeries.actionSeries:
                if action.actionName == 'TASK_BEGIN':
                    _h = int(action.attributes['contentheight'])
                    contentheight.append(_h)
#2367.18
print np.mean(contentheight)