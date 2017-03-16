# coding=utf8
__author__ = 'luocheng'
__date__ = '12/12/2016-3:30 PM'
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

from  bs4 import BeautifulSoup
from utils import *

# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

id2query = load_id2query()


class Result:
    def __init__(self, topicid, source, matched_id, top, bottom, left, right, text, code):
        self.topicid = topicid

        self.source = source
        self.matched_id = matched_id
        self.top = float(top)
        self.bottom = float(bottom)
        self.left = float(left)
        self.right = float(right)
        self.text = text
        self.code = code
        self.url = None
        self.clickScore = 0
        self.query = id2query[self.topicid]

    def dump(self):
        output = [self.topicid, self.query, self.source, self.matched_id, self.top, self.bottom, self.clickScore,
                  self.url]
        return '\t'.join([str(item) for item in output])


def getUrlForEachResult():
    annotation = load_content()
    query2id = load_query2id()
    id2query = load_id2query()
    annotated_url = dict()
    for item in annotation:
        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments = item[0:10]
        qid = query2id[query]
        annotated_url[(qid, source, rank)] = result_url

    def extractAnchor(code):
        try:
            anchors = []
            soup = BeautifulSoup(code, 'html.parser')
            for a in soup.findAll('a'):
                if a.has_attr('href'):
                    anchors.append(a['href'])
            return anchors
        except:
            return []

    results = []
    for source in ['sogou', 'baidu', 'sm', 'haosou']:
        import os
        for f in [item for item in os.listdir('../newdata/match/' + source) if '.txt' in item]:
            topicid, source = f.split('.')[0:2]
            for l in open('../newdata/match/' + source + '/' + f).readlines():
                segs = l.strip().split('\t')
                matchedid = segs[1]
                if matchedid not in '12345':
                    continue
                if len(segs) >= 6:
                    left, right, top, bottom = segs[2], segs[3], segs[4], segs[5]
                    if len(segs) >= 7:
                        text = segs[6]
                    else:
                        text = ''

                    if len(segs) >= 8:
                        code = segs[7]
                    else:
                        code = ''

                    result = Result(topicid, source, matchedid, top, bottom, left, right, text, code)
                    result.url = annotated_url[(topicid, source, matchedid)]
                    if result.url == "None":
                        anchors = extractAnchor(result.code)
                        if anchors:
                            result.url = anchors[0]

                    results.append(result)

    fout = open('../newdata/allresults.tsv', 'w')
    for r in results:
        fout.write(r.dump() + '\n')
    fout.close()


def url2screenshot(url, filename):
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=d)
    driver.set_window_size(360, 440)

    # from selenium.webdriver import Firefox
    # driver = Firefox()
    # driver.set_window_position(0, 0)
    # driver.set_window_size(360, 440)
    driver.set_page_load_timeout(120)
    try:
        driver.get(url)

    except:
        print 'exception', url
    finally:
        driver.get_screenshot_as_file(filename)
        driver.close()


def getPageLength(filename):
    content = open(filename).read()
    import re
    pat = re.compile('\"document.body.scrollHeight\":[ ]*(\d*),')
    match = re.search(pat, content)
    if match:
        return match.group(1)

    return None


def getSreenshotOfLandingPage():
    script = open('./batchPhan.bat', 'w')
    height = open('../newdata/landingpage_height.txt', 'w')
    for l in open('../newdata/allresults.fixed.tsv').readlines()[1:]:
        segs = l.strip().split('\t')
        queryid = segs[0]
        query = segs[1]
        source = segs[2]
        rank = segs[3]
        url = segs[7]
        heightfile = '../newdata/landingpage_screenshot/' + queryid + '-' + source + '-' + rank + '.txt'
        heightfile_name = queryid + '-' + source + '-' + rank + '.txt'
        pngfile = '../newdata/landingpage_screenshot/' + queryid + '-' + source + '-' + rank + '.png'
        import os
        if heightfile_name in os.listdir('../newdata/landingpage_screenshot'):
            if getPageLength(heightfile):
                height.write(queryid + '-' + source + '-' + rank + '\t' + getPageLength(heightfile) + '\n')
                continue

        if url.startswith('http'):
            print url
            import os
            try:
                script.write("phantomjs getheight.js " + url + ' > ' + heightfile + '\n')

                # os.system("phantomjs getheight.js "+url+' > '+heightfile)
                # import time
                # time.sleep(10)
                # print url
                # os.system("phantomjs url2page.js "+url+' '+pngfile)
                # # os.system("phantomjs crawl.js "+htmlfile +' '+pngfile)
            except:
                print 'EXCEPTION', url
    script.close()


def incorporateHeight():
    from collections import defaultdict
    result2height = defaultdict(lambda: '-1')
    for l in open('../newdata/landingpage_height.txt'):
        name, height = l.strip().split('\t')
        result2height[name] = height

    fout = open('../newdata/allresult.fixed.withheight.tsv', 'w')
    fout.write('queryid\tquery\tsource\trank\ttop\tbottom\tscore\turl\tresult_height\n')
    for l in open('../newdata/allresults.fixed.tsv').readlines()[1:]:
        queryid, query, source, rank, top, bottom, score, url = l.strip().split('\t')
        resultname = queryid + '-' + source + '-' + rank
        height = result2height[resultname]
        fout.write('\t'.join([queryid, query, source, rank, top, bottom, score, url, height]) + '\n')
    fout.close()


def loadHeight():
    allresult = []
    longpages = []

    for l in open('../newdata/allresult.fix.withheight.tsv').readlines()[1:]:
        queryid, query, source, rank, top, bottom, score, url, height = l.strip().split('\t')
        height = int(height)
        queryid = '0' * (4 - len(queryid)) + queryid
        allresult.append([queryid, source, rank, url, height])
        if int(height) >= 667:
            longpages.append(int(height))
    import numpy
    mean = int(numpy.mean(longpages))
    for item in allresult:
        queryid, source, rank, url, height = item
        if url == "None":
            continue
        else:
            if height == 300:
                item[-1] = mean
            elif height < 667:
                item[-1] == mean
    ht = dict()
    for item in allresult:
        queryid, source, rank, url, height = item
        ht[(queryid, source, rank)] = height
    return ht


def intergrateData():
    # height:  key : queryid, source, rank
    # * score, * serpheight, * landing height, *necessity

    # landingHeight
    landingHeight = loadHeight()
    serpHeight = dict()
    for l in open('../newdata/allresult.fix.withheight.tsv').readlines()[1:]:
        queryid, query, source, rank, top, bottom, score, url, _ = l.strip().split('\t')
        queryid = '0' * (4 - len(queryid)) + queryid

        serpHeight[(queryid, source, rank)] = float(bottom) - float(top)

    # score of result , necessity
    resultScore = dict()
    resultNecessity = dict()
    from utils import load_content, load_query2id
    contents = load_content()
    q2id = load_query2id()
    for item in contents:
        print len(item)
        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments, _, _, necess = item
        qid = q2id[query]
        resultScore[(qid, source, rank)] = int(float(score) + 0.5)
        resultNecessity[(qid, source, rank)] = int(necess)

    # output
    fout = open('../newdata/everything_for_metrics.tsv', 'w')
    for qid in range(1, 51, 1):
        qid = '0' * (4 - len(str(qid))) + str(qid)
        for source in ['baidu', 'sogou', 'haosou', 'sm']:
            for rank in '12345':
                k = (qid, source, rank)
                fout.write('\t'.join([str(item) for item in
                                      [qid, source, rank, resultScore[k], resultNecessity[k], int(serpHeight[k]),
                                       int(landingHeight[k])]]))
                fout.write('\n')
    fout.close()


#      each result: qid, source, rank, score, necessity, serpheight,landingheigh
def evl_orig(sheight, lheight, relevance, necessity):
    origpossibility = [[0.4025974025974026, 0.06666666666666667, 0.09340659340659341],
                       [0.4379391100702576, 0.31343283582089554, 0.039603960396039604],
                       [0.5, 0.6067961165048543, 0.147239263803681],
                       [0.6474820143884892, 0.8837209302325582, 0.7566666666666667]]

    # p_click_rel = [0.281188118812, 0.35630252100, 0.458479532164, 0.734702992407]
    # n = {2: 0.0, 1: 1.0, 0: 1.0}

    r = {0: 1, 2: 2, 3: 3, 4: 4, 5: 4}
    expected_lp_length = origpossibility[r[relevance] - 1 ][necessity] * lheight
    expected_lp_length = int(expected_lp_length)
    return sheight, expected_lp_length, sheight+expected_lp_length

def evl_modi(sheight, lheight, relevance, necessity):
    possibility = [[0.402597403, 0.066666667, 0.093406593],
                   [0.43793911, 0.313432836, 0.03960396],
                   [0.606796117, 0.5, 0.147239264],
                   [0.88372093, 0.756666667, 0.647482014]]

    # p_click_rel = [0.281188118812, 0.35630252100, 0.458479532164, 0.734702992407]
    # n = {2: 0.0, 1: 1.0, 0: 1.0}

    r = {0: 1, 2: 2, 3: 3, 4: 4, 5: 4}
    expected_lp_length = possibility[r[relevance] - 1 ][necessity] * lheight
    expected_lp_length = int(expected_lp_length)
    return sheight, expected_lp_length, sheight+expected_lp_length



def generateGainDistribution(score, sheight, expected_lp_height):

    if  expected_lp_height == 0:
        return [float(score) / float(sheight)] * int(sheight)
    else:
        gain1 = [0.4 * float(score) / float(sheight)] * int(sheight)
        gain2 = [0.6 * float(score) / float(expected_lp_height)] * expected_lp_height

        return gain1 + gain2


# @parameters  results: a list of the top 5 results, each result has
#             qid, source, rank, score, necessity, serpHeight, landingHeight
#
#
#             decayfunc:  a function pointer

def PBG(results, decayfunc, evlfunc):
    # possibility[relevance 0,1,2,3][necessity 0,1,2]
    start = 0
    gain = 0
    for item in results:
        qid, source, rank, score, necessity, serpHeight, landingHeight = item
        score = int(score)
        necessity = int(necessity)
        serpHeight = int(serpHeight)
        landingHeight = int(landingHeight)
        _sheight, _expected_lp_length, _evl = evlfunc(sheight=serpHeight, lheight=landingHeight, relevance=score, necessity=necessity)
        _evl = int(_evl)
        gaindist = generateGainDistribution(score, _sheight, _expected_lp_length)
        for i in range(_evl):
            gain += gaindist[i] * decayfunc(start + i)
        start += _evl
    return gain


def nPBG(results, decayfunc,evlfunc):
    origScore = PBG(results, decayfunc,evlfunc)
    idealResults = []
    for item in results:
        _item = item[:]
        _item[3] = 5
        idealResults.append(_item)
    idealScore = PBG(idealResults, decayfunc,evlfunc)
    return origScore / idealScore


def calibratedDecay(p):
    import math
    return math.e ** ((-1.0) * math.log(2) * p / 10069.13)


def pk_hcs_leave_possibility(_lambda, _miu, K):
    from scipy.stats import norm
    import math
    # https: // en.wikipedia.org / wiki / Inverse_Gaussian_distribution
    if K == 0:
        K = 1
    first = (_lambda / K) ** 0.5 * (K / _miu - 1.0)

    second = 2.0 * _lambda / _miu
    third = (-1.0) * (_lambda / K) ** 0.5 * (K / _miu + 1.0)
    cdf = norm.cdf(first) + math.exp(second) * norm.cdf(third)
    return 1 - cdf


def hcsDecay(position):
    _lambda = 23070.1
    _miu = 13510.1
    return pk_hcs_leave_possibility(_lambda, _miu, position)


def calculatePBG(decayfunc, evlfunc, pbgfilename, npbgfilename):
    from collections import defaultdict
    results = defaultdict(lambda: [])
    for l in open('../newdata/everything_for_metrics.tsv').readlines():
        qid, source, rank, score, necessity, serpHeight, landingHeight = l.strip().split('\t')
        rank = int(rank)
        score = int(score)
        necessity = int(necessity)
        serpHeight = int(float(serpHeight))
        landingHeight = int(float(landingHeight))

        results[(qid, source)].append([qid, source, rank, score, necessity, serpHeight, landingHeight])
    pbgout = open('../newdata/'+pbgfilename, 'w')
    npbgout = open('../newdata/'+npbgfilename, 'w')

    count = 0
    for k in results:
        results[k].sort(key=lambda x: x[2])

        qid, source = k
        pbg = PBG(results[k], decayfunc, evlfunc )
        npbg = nPBG(results[k], decayfunc, evlfunc)
        pbgout.write('\t'.join([qid, source, str(pbg)]) + '\n')
        npbgout.write('\t'.join([qid, source, str(npbg)]) + '\n')
        print count , qid, source, pbg, npbg
        count +=1


def calculatePBG_debug(decayfunc, evlfunc,_qid, _source):
    from collections import defaultdict
    results = defaultdict(lambda: [])
    for l in open('../newdata/everything_for_metrics.tsv').readlines():
        qid, source, rank, score, necessity, serpHeight, landingHeight = l.strip().split('\t')
        rank = int(rank)
        score = int(score)
        necessity = int(necessity)
        serpHeight = int(float(serpHeight))
        landingHeight = int(float(landingHeight))

        results[(qid, source)].append([qid, source, rank, score, necessity, serpHeight, landingHeight])

    for k in results:
        results[k].sort(key=lambda x: x[2])
        qid, source = k
        if qid == _qid and source == _source:
            pbg = PBG(results[k], decayfunc, evlfunc )
            npbg = nPBG(results[k], decayfunc, evlfunc)
            print qid, source, pbg, npbg



if __name__ == '__main__':
    # getSreenshotOfLandingPage()
    # print getPageLength('../newdata/landingpage_screenshot/2-sm-2.txt')

    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == '1':
            calculatePBG(calibratedDecay, evl_orig, 'pbg_tbg_orig.tsv', 'npbg_tbg_orig.tsv')
        if sys.argv[1] == '2':
            calculatePBG(calibratedDecay, evl_modi, 'pbg_tbg_modi.tsv', 'npbg_tbg_modi.tsv')
        if sys.argv[1] == '3':
            calculatePBG(hcsDecay, evl_orig, 'pbg_hcs_orig.tsv', 'npbg_hcs_orig.tsv')
        if sys.argv[1] == '4':
            calculatePBG(hcsDecay, evl_modi, 'pbg_hcs_modi.tsv', 'npbg_hcs_modi.tsv')
    if len(sys.argv) == 3:
        calculatePBG_debug(hcsDecay, evl_modi, sys.argv[1], sys.argv[2])