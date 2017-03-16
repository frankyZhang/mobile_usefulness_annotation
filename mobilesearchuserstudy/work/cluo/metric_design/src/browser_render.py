
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from utils import load_content, load_query2id
import urllib
# enable browser logging
import os
def render_by_browser():
    for f in os.listdir('../data/sogou_sbs_page_source'):
        if '.html' in f:
            print f

            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = { 'browser':'ALL' }
            driver = webdriver.Chrome(desired_capabilities=d)
            driver.set_window_size(360,440)

            try:
                fout = open('../data/browser_render_jsoutput/' + f.replace('.html', '.txt'), 'w')
                driver.get('http://127.0.0.1:8000/'+f)
                # print messages
                for entry in driver.get_log('browser'):
                    segs = entry['message'].split(' ')
                    fout.write(' '.join(segs[2:]))
                driver.close()
                fout.close()
            except:
                print 'Exception',f
def compact_js_output():
    for f in os.listdir('../data/browser_render_jsoutput'):
        status = 0
        position  = ''
        content  = ''
        _position = []
        _content = []
        
        for l in open('../data/browser_render_jsoutput/'+f):
            l = l.strip()
            # print status
            if status == 0:
                if l == '<position>':
                    status = 1
                else:
                    pass
                continue
            if status == 1:
                if len(l.strip().split(' ')) == 5:
                    position = ' '.join(l.strip().split(' ')[1:])
                    status =2
                continue
                
            if status == 2:
                if l == '</position>':
                    status = 3
                else:
                    pass
                continue
                
            if status == 3:
                if l == '<nodecontent>':
                    status =4
                else:
                    pass
                continue
                
            if status == 4:
                if '</nodecontent>' in l:
                    content += ' '+l.replace('</nodecontent>','')
                    _position.append(position)
                    _content.append(content)
                    position = ''
                    content = ''
                    status = 0
                else:
                    content += ' '+ l
                continue
        fout = open('../data/browser_render_jsoutput_dense/'+f,'w')
        for i in range(len(_position)):
            fout.write(_position[i]+'\n')
            fout.write(_content[i]+'\n')
        fout.close()




def parse_serp_sogou(filename):
    content = open(filename).read()
    soup = BeautifulSoup(content, 'html.parser')
    divblock = soup.find('div',class_='results')
    divlist = divblock.children
    idx = 1
    fout = open('../data/temp/'+filename.split('/')[-1].replace('.html','.txt'),'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':
            rtr.append((idx,extract_content(str(d)), compact_html(str(d))))
            idx +=1
    return rtr
    
def parse_serp_baidu(filename):
    content = open(filename).read()
    soup = BeautifulSoup(content, 'html.parser')
    divblock = soup.find('div',id='results')
    divlist = soup.find_all('div', class_='result')
    print len(divlist)
    idx = 1
    fout = open('../data/temp/'+filename.split('/')[-1].replace('.html','.txt'),'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':
            rtr.append((idx,extract_content(str(d)), compact_html(str(d) ) ))
            fout.write(str(idx) + '\t' + extract_content(str(d)) + '\n')
            idx +=1
    return rtr

def parse_serp_sm(filename):
    content = open(filename).read()
    soup = BeautifulSoup(content,'html.parser')
    divblock = soup.find('div',id='results')
    divlist = divblock.children
    idx = 1
    # fout = open('../data/temp/'+filename.split('/')[-1].replace('.html','.txt'),'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':

            rtr.append((idx,extract_content(str(d)), compact_html(str(d))))
            # fout.write(str(idx)+'\t'+extract_content(str(d))+'\n')
            idx +=1
    return rtr

def parse_serp_haosou(filename):
    content = open(filename).read()
    soup = BeautifulSoup(content, 'html.parser')
    divblock = soup.find('div', class_='r-results')
    divlist = divblock.children
    idx = 1
    # fout = open('../data/temp/' + filename.split('/')[-1].replace('.html', '.txt'), 'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':
            rtr.append((idx, extract_content(str(d)), compact_html(str(d))))
            # fout.write(str(idx) + '\t' + extract_content(str(d)) + '\n')
            idx += 1
    return rtr


    
def contact_align(filter):
    parser_map = {'sogou':parse_serp_sogou, 'sm':parse_serp_sm, 'haosou':parse_serp_haosou, 'baidu':parse_serp_baidu}
    for f in os.listdir('../data/sogou_sbs_page_source'):
        if '.html' in f and filter in f:
            print f
            qid, source = f.replace('.html','').split('_')
            parser = parser_map[source]

            results_on_serp  = parser('../data/sogou_sbs_page_source/'+f)

            position_on_serp =  dict()

            lines = open('../data/browser_render_jsoutput_dense/'+f.replace('.html','.txt')).readlines()
            for i in range(0,len(lines)/2,1):
                segs = lines[2*i].strip().split(' ')
                left, right, top,bottom = segs[0], segs[1], segs[2], segs[3]
                html =  extract_content(lines[2*i+1].strip())
                position_on_serp[html] = (left,right,top,bottom)

            content = load_content()
            query2id = load_query2id()
            content_of_this = [item for item in content if  item[1] == source and query2id[item[0]] == qid]

            fout = open('../data/match_raw/'+f.replace('.html','.match.tsv'),'w')
            for ros in results_on_serp:

                idx, result_text, raw_html = ros
                l, r, t, b = 'None', 'None', 'None', 'None'
                if result_text in position_on_serp:
                    l,r,t,b = position_on_serp[result_text]
                resultidx = 'None'
                for item in content_of_this:
                    query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments = item

                    if len(result_url)> 0 and (result_url in raw_html or urllib.quote(result_url,'') in raw_html):
                        resultidx = str(rank)



                fout.write('\t'.join([str(item) for item in [resultidx, idx, l,r,t,b,result_text]]))
                fout.write('\n')
            fout.close()
contact_align('sm')


