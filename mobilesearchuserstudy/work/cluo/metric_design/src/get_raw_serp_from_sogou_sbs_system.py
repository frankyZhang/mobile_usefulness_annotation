#coding=utf8

from utils import *
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf8')

contents = load_content()
query2id = load_query2id()
# query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments
urls = set()
for item in contents:
    query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments = item
    queryid = query2id[query]

    urls.add( (queryid,source, url))

fout = open('../data/sogou_system_urls.tsv','w')

urls = list(urls)
urls.sort(key= lambda x: x[0])
for queryid, source,result_url in urls:
    if result_url != '':
        fout.write(queryid+'\t'+source+'\t'+result_url+'\n')
fout.close()



all_sources = set()
from bs4 import BeautifulSoup
for l in open('../data/sogou_system_urls.tsv'):
    queryid, source,url = l.strip().split('\t')

    u = urllib2.urlopen(url,timeout=100)
    content = u.read()
    soup = BeautifulSoup(content,'html.parser')
    for frame in soup.find_all('iframe'):
        href ='http://sbs.m.sogou.com' + frame['src']
        site = ''
        for s in href.split('&'):
            if 'site=' in s:
                site = s.replace('site=','')
                break
        if site!= '':
            all_sources.add( ( queryid, site, href))

fout = open('../data/urls.tsv','w')
for qid,st, u in all_sources:
    fout.write('\t'.join([qid,st,u])+'\n')
fout.close()

for l in open('../data/urls.tsv'):
    qid, source, url =l.strip().split('\t')
    fout = open('../data/sogou_sbs_page_source/'+ qid+'_'+source+'.html','w')
    fout.write(urllib2.urlopen(url,timeout=100).read())
    fout.close()





