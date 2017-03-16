#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup


import os
injected_js = open('../data/injected.js').read()
psh = open('phantom_render.sh','w')


for f in os.listdir('../data/sogou_sbs_page_source'):
    if '.html' in f:
        print f
        content = open('../data/sogou_sbs_page_source/'+f).read()
        if '</html>' not in content:
            print 'Exception', f, '<> not found'
            print content
        else:
            content = content.replace('</html>', '</html>\n'+injected_js)

            if 'sogou' in f:
                soup = BeautifulSoup(content,'html.parser')
                for s in soup.find_all('script'):
                    if '/resource/vr/common/service.vr' in s.get_text():
                        s.clear()
                        break
                open('../data/sogou_sbs_page_source_injected/' + f, 'w').write(soup.prettify())

            else:
                open('../data/sogou_sbs_page_source_injected/'+f,'w').write(content)
            psh.write('phantomjs render.js http://127.0.0.1:8000/'+f+' > ../data/element_position_raw/'+f.replace('.html','.txt')+'\n')
psh.close()

