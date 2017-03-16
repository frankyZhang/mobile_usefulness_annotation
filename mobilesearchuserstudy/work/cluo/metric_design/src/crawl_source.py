#coding=utf8
from utils import *
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf8')

for l in open('../data/urls.tsv'):
    qid, source, url =l.strip().split('\t')
    fout = open('../data/sogou_sbs_page_source/'+ qid+'_'+source+'.html','w')
    fout.write(urllib2.urlopen(url,timeout=100).read())
    fout.close()
