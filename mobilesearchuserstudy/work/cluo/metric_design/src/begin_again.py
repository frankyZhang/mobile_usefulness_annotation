import HTMLParser
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from utils import load_content, load_query2id
import urllib


def crawl_raw_source_with_selenium():
    finished = os.listdir('../newdata/page_source')
    for l in open('../data/urls.tsv'):

        qid, source, url = l.strip().split('\t')
        if '.'.join([qid,source,'html']) in finished:
            continue

        print qid, source
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = { 'browser':'ALL' }
        driver = webdriver.Chrome(desired_capabilities=d)
        driver.set_window_size(360,440)

            # load some site
        try:
            fout = open('../newdata/page_source/'+'.'.join([qid, source, 'html']),'w')
            driver.get(url)
            fout.write(driver.page_source)

            fout.close()
        except:
            print 'Exception',qid,source
        finally:
            driver.close()


def inject_serp_with_js():
    injected_js = open('../newdata/injected.js').read()

    for f in os.listdir('../newdata/page_source'):
        if '.html' in f:
            print f
            import HTMLParser

            content = HTMLParser.HTMLParser().unescape(open('../newdata/page_source/' + f).read())
            if '</html>' not in content:
                print 'Exception', f, '</html> not found'
                print content
            else:
                content = content.replace('</html>', '</html>\n' + injected_js)
                if 'sogou' in f:
                    soup = BeautifulSoup(content, 'html.parser')
                    for s in soup.find_all('script'):
                        if '/resource/vr/common/service.vr' in s.get_text():
                            s.clear()
                            break
                    open('../newdata/page_source_injected/' + f, 'w').write(soup.prettify())

                else:
                    open('../newdata/page_source_injected/' + f, 'w').write(content)


def get_js_raw_output_by_rendering_in_browser(filter):
    for f in os.listdir('../newdata/page_source_injected'):
        if '.html' in f and filter  in f:
            print f

            d = DesiredCapabilities.CHROME
            d['loggingPrefs'] = { 'browser':'ALL' }
            driver = webdriver.Chrome(desired_capabilities=d)
            driver.set_window_size(360,440)

            # load some site
            try:
                driver.get('http://127.0.0.1:8000/'+f)
                # print messages
                fout = open('../newdata/browser_render_jsoutput/' + f.replace('.html', '.txt'), 'w')
                for entry in driver.get_log('browser'):
                    segs = entry['message'].split(' ')
                    fout.write(' '.join(segs[2:]))
                fout.close()
            except:
                print 'Exception',f
            finally:
                driver.close()


def extract():
    rtr = dict()
    for f in os.listdir('../newdata/browser_render_jsoutput'):
        if '.txt' not in f:
            continue
        positionout = open('../newdata/position/'+f,'w')
        qid, source = f.replace('.txt','').split('.')
        print qid, source
        status = 0
        position = ''
        content = ''
        _position = []
        _content = []
        thisfile = []
        for l in open('../newdata/browser_render_jsoutput/' + f):
            l = l.strip()
            if status == 0:
                if l == '<position>':
                    status = 1
                else:
                    pass
                continue
            if status == 1:
                if len(l.strip().split(' ')) == 4:
                    position = l.strip()
                    status = 2
                continue

            if status == 2:
                if l == '</position>':
                    status = 3
                else:
                    pass
                continue

            if status == 3:
                if l == '<nodecontent>':
                    status = 4
                else:
                    pass
                continue

            if status == 4:
                if '</nodecontent>' in l:

                    content += ' ' + l.replace('</nodecontent>', '')

                    # _position.append(position)
                    # _content.append(content)
                    if content.strip().startswith('<div'):
                        soup = BeautifulSoup(content, 'html.parser')
                        thisfile.append([position, soup])
                        positionout.write(position+'\n'+str(soup).replace('\n',' ')+'\n')

                    position = ''
                    content = ''
                    status = 0
                else:
                    content += ' ' + l
                continue

        rtr[qid+'.'+source] = thisfile
        positionout.close()
    return rtr
        # fout = open('../data/browser_render_jsoutput_dense/' + f, 'w')
        # for i in range(len(_position)):
        #     fout.write(_position[i] + '\n')
        #     fout.write(_content[i] + '\n')
        # fout.close()


def parse_serp_sogou(filename):
    content = HTMLParser.HTMLParser().unescape(open(filename).read())
    soup = BeautifulSoup(content, 'html.parser')
    divblock = soup.find('div', class_='results')
    divlist = divblock.children
    idx = 1
    fout = open('../data/temp/' + filename.split('/')[-1].replace('.html', '.txt'), 'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':
            rtr.append((idx, extract_content(str(d)), d))
            idx += 1
    return rtr


def parse_serp_baidu(filename):
    content = HTMLParser.HTMLParser().unescape(open(filename).read())
    soup = BeautifulSoup(content, 'html.parser')
    divblock = soup.find('div', id='results')
    divlist = soup.find_all('div', class_='result')
    idx = 1
    fout = open('../data/temp/' + filename.split('/')[-1].replace('.html', '.txt'), 'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':
            rtr.append((idx, extract_content(str(d)), d))
            fout.write(str(idx) + '\t' + extract_content(str(d)) + '\n')
            idx += 1
    return rtr


def parse_serp_sm(filename):
    content = HTMLParser.HTMLParser().unescape(open(filename).read())
    soup = BeautifulSoup(content, 'html.parser')
    divblock = soup.find('div', id='results')
    divlist = divblock.children
    idx = 1
    # fout = open('../data/temp/'+filename.split('/')[-1].replace('.html','.txt'),'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':
            rtr.append((idx, extract_content(str(d)), d))
            # fout.write(str(idx)+'\t'+extract_content(str(d))+'\n')
            idx += 1
    return rtr


def parse_serp_haosou(filename):
    content = HTMLParser.HTMLParser().unescape(open(filename).read())
    soup = BeautifulSoup(content, 'html.parser')
    divblock = soup.find('div', class_='r-results')
    divlist = divblock.children
    idx = 1
    # fout = open('../data/temp/' + filename.split('/')[-1].replace('.html', '.txt'), 'w')
    rtr = []
    for d in divlist:
        if d.name == 'div':
            rtr.append((idx, extract_content(str(d)), d))
            # fout.write(str(idx) + '\t' + extract_content(str(d)) + '\n')
            idx += 1
    return rtr


def align_new(filter):
    parser_map = {'sogou': parse_serp_sogou, 'sm': parse_serp_sm, 'haosou': parse_serp_haosou,
                  'baidu': parse_serp_baidu}

    annotation = load_content()

    query2id = load_query2id()
    all_position = load_position(filter)
    # from collections import defaultdict
    # all_position = defaultdict(lambda:[])
    for f in os.listdir('../newdata/page_source'):
        if filter not in f:
            continue
        if '.html' in f:
            qid, source = f.replace('.html', '').split('.')
            parser = parser_map[source]
            results_on_serp = parser('../newdata/page_source/' + f)
            print f,len(results_on_serp)
            content_of_this = [item for item in annotation if item[1] == source and query2id[item[0]] == qid]
            fout = open('../newdata/match/'+f.replace('.html','.txt'),'w')
            count = 0
            for r in results_on_serp:
                count +=1
                result_idx, text,d = r
                position = 'None\tNone\tNone\tNone'
                matched_idx = 'None'
                for p in all_position[qid+'.'+source]:
                    _p, _d = p
                    if twoNodeEqual(d,_d,filter):
                        position = _p.strip().replace(' ','\t')
                    for item in content_of_this:
                        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments = item
                        if result_url in str(d):
                            matched_idx = str(rank)
                            break
                fout.write('\t'.join([str(count), matched_idx , position,d.get_text().strip().replace('\n',' ').replace('\t',''),str(d).replace('\n',' ').replace('\t',' ')]))
                fout.write('\n')
            fout.close()

def compact_html(content):
    for c in '\n\t ':
        content = content.replace(c,'')
    return content

def extract_content(content):
    sp = BeautifulSoup(content,'html.parser')
    for s in sp.find_all('script'): s.clear()
    for s in sp.find_all('style'):s.clear()
    return compact_html(sp.get_text())


def test():
    source = 'A&amp;B'
    import HTMLParser
    s =  HTMLParser.HTMLParser().unescape(source)
    print s,source

def twoNodeEqual(nodea, nodeb,filter):
    # print '-----'
    ignore_attr_list = ['data-img-loaded']


    if nodea.name != 'div':
        nodea = nodea.find('div')
    if nodeb.name != 'div':
        nodeb = nodeb.find('div')


    for node in [nodea,nodeb]:
        for s in node.find_all('script'): s.clear()
        for s in node.find_all('style'): s.clear()
    # print 'a',nodea.attrs
    # print 'a',nodeb.attrs
    for a in nodea.attrs:
        if a in nodeb.attrs:
            if a in ignore_attr_list:continue
            if nodea[a] == nodeb[a]:
                pass
            else:
                # print 'attr value not match', nodea[a], nodeb[a]
                return False
        else:
            # print 'attr not match a->b'
            return False
    for a in nodeb.attrs:
        if a in ignore_attr_list: continue
        if a in nodea.attrs:
            if nodea[a] != nodeb[a]:
                # print 'attr value not match', nodea[a], nodeb[a]
                return False
        else:
            # print 'attr not match b->a'
            return False

    texta = nodea.get_text()
    textb = nodeb.get_text()

    for c in '\t\n ':
        texta.replace(c, '')
        textb.replace(c, '')
    texta = texta.replace(' ', '')
    textb = textb.replace(' ', '')
    if filter != 'sogou':
        if texta != textb:
            # print 'text not exactly match'
            return False
    else:
        if jsimilartiy(texta, textb)<0.9:
            # print 'text inconsistent',jsimilartiy(texta, textb)
            return False
    return True

def jsimilartiy(l1, l2):
    all = set()
    for item in l1: all.add(item)
    for item in l2: all.add(item)
    count = 0
    for item in all:
        if item in l1 and item in l2:
            count +=1
    return float(count)/float(len(all))

def load_position(filter):
    rtr = dict()
    for f in os.listdir('../newdata/position'):
        if '.txt' in f and filter in f:
            print 'load position',f
            lines = open('../newdata/position/'+f).readlines()
            current_page = []
            for i in range(0, len(lines)/2,1):
                position = lines[2*i].strip()
                node = BeautifulSoup(lines[2*i+1].strip(), 'html.parser')
                current_page.append([position, node])
            rtr[f.replace('.txt','')] = current_page
    return rtr


def test_single_case(filter):
    all_position = dict()
    for f in ['0001.sogou.txt']:
        if '.txt' in f and filter in f:
            print 'load position', f
            lines = open('../newdata/position/' + f).readlines()
            current_page = []
            for i in range(0, len(lines) / 2, 1):
                position = lines[2 * i].strip()
                node = BeautifulSoup(lines[2 * i + 1].strip(), 'html.parser')
                current_page.append([position, node])
            all_position[f.replace('.txt', '')] = current_page
    parser_map = {'sogou': parse_serp_sogou, 'sm': parse_serp_sm, 'haosou': parse_serp_haosou,
                  'baidu': parse_serp_baidu}

    annotation = load_content()

    query2id = load_query2id()
    # from collections import defaultdict
    # all_position = defaultdict(lambda:[])
    for f in ['0001.sogou.html']:
        if filter not in f:
            continue
        if '.html' in f:
            qid, source = f.replace('.html', '').split('.')
            parser = parser_map[source]
            results_on_serp = parser('../newdata/page_source/' + f)
            print f, len(results_on_serp)
            content_of_this = [item for item in annotation if item[1] == source and query2id[item[0]] == qid]
            fout = open('../newdata/match/' + f.replace('.html', '.txt'), 'w')
            count = 0
            for r in results_on_serp:
                count += 1
                result_idx, text, d = r
                position = 'None\tNone\tNone\tNone'
                matched_idx = 'None'
                for p in all_position[qid + '.' + source]:
                    _p, _d = p
                    print twoNodeEqual(d,_d)
                    if twoNodeEqual(d, _d):
                        print 'Bingo!!!', _p
                        position = _p.strip().replace(' ', '\t')
                    for item in content_of_this:
                        query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments = item
                        if result_url in str(d):
                            matched_idx = str(rank)
                            break
                fout.write('\t'.join(
                    [str(count), matched_idx, position, d.get_text().strip().replace('\n', ' ').replace('\t', ''),
                     str(d).replace('\n', ' ').replace('\t', ' ')]))
                fout.write('\n')
            fout.close()


def test_node():

    d1 = BeautifulSoup(open('../newdata/node1.txt').read(),'html.parser')
    d2 = BeautifulSoup(open('../newdata/node2.txt').read(),'html.parser')
    d1 = d1.find('div')
    d2 = d2.find('div')

    print twoNodeEqual(d1,d2)


if __name__ == "__main__":
    test_single_case('baidu')