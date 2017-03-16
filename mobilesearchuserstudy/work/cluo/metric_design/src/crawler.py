
import urllib
import os

url_set = set()

for f in os.listdir('../data/sogou_sbs_page_source'):
    if '.html' in f:
        pagefile = '../data/sogou_sbs_page_source/' + f
        pngfile = '../data/serp_screenshots/' + f.replace('.html', '.png')
        command = 'phantomjs crawl.js '+pagefile+' '+pngfile
        print command
        os.system(command)
'''
fin = open('links.txt', 'r')
for url in fin:
    url = url.rstrip()
    if url in url_set:
        continue
    url_set.add(url)
    query = url.split('/')[-3]
    page_id = url.split('/')[-2]
    command = 'phantomjs.exe crawl.js "%s" "screen_shot/%s_%s.png"' % (url, query, page_id)
    print command
    os.system(command)

'''