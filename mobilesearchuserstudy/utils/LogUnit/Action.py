#coding=utf8

__author__='luocheng'


class Action:
    def __init__(self):
        self.timeStamp = 0
        self.task = ''
        self.actionName = ''
        self.attributes = dict()

    def parseFromLine(self,line):
        segs = line.strip().split('\t')

        self.timeStamp = int(segs[0].split('=')[1])

        if segs[1].split('=')[1] == '':
            self.task = None
        else:
            self.task = int(segs[1].split('=')[1])

        self.actionName= segs[2].split('=')[1]

        idx = line.find('INFO:')
        line = line[idx+6:]
        for s in line.strip().split('\t'):
            _segs =s.split('=')
            if len(_segs) >= 2:
                k = _segs[0]
                self.attributes[k] = '='.join(_segs[1:])

if __name__=="__main__":
    action = Action()
    log = 'TIME=1477104306885	Task=18	ACTION=CLICK_RESULT	INFO:	URL=http://m.so.com/jump?u=http%3A%2F%2Fwapbaike.baidu.com%2Fview%2F873475.htm&m=4edd52&from=&words=%E7%98%B8%E5%AD%90&monitor=pro%3Dm_so%26pid%3Dresult%26u%3Dhttp%253A%252F%252F10.129.248.85%253A8000%252Fsearch%252F2013010932%252F1%252F18%252F%26guid%3D225657114.613588324077547900.1477104298948.2776%26mbp%3D1%26q%3D%25E5%258F%25A4%25E7%2590%25B4%25E4%25BB%25B7%25E6%25A0%25BC%26pq%3D%26ls%3D%26src%3D%26abv%3D-%26sid%3D61cdd698726d75e0ab0b01906fb49452%26srcg%3D%26userid%3D%26version%3D%26category%3D%26folding%3D0%26folding_type%3D%26nettype%3Dunknown%26mode%3D1%26mod%3Dog%26cat%3D%26pos%3D10%26pn%3D1%26type%3Dwap%26data-md-b%3Dtitle%26clicktype%3Dlink%26value%3Dhttp%253A%252F%252Fwapbaike.baidu.com%252Fview%252F873475.htm%26t%3D1477104306861'
    action.parseFromLine(log)
    print  action.timeStamp,action.task, action.actionName
    for k in action.attributes:
        print k, action.attributes[k]
