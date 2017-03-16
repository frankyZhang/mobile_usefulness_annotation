import sys
reload(sys)
sys.setdefaultencoding('utf8')
from openpyxl import load_workbook


wb2 = load_workbook('../docs/top5_50_0919.xlsx')
sheet1 = wb2.get_sheet_by_name(u'top5')


fout = open('../data/top5_50_0919.tsv','w')

contents = []
for r in range(2, 1002,1):
    line = []
    for c in 'ABCDEFGHIJ':
        if c == 'C':
            try:
                val = sheet1[c+str(r)].hyperlink.display
            except:
                val = ''
        else:
            val = str(sheet1[c+str(r)].value)
        line.append(val)
    contents.append(line)
for item in contents:
    fout.write('\t'.join(item)+'\n')
fout.close()



queries = list()
for l in contents:
    query, source, url, result_url, type, rank, score, comments,sbs, sbs_comments = l

    if query in queries:
        continue
    else:
        queries.append(query)
query2id = dict()
idx = 1
query_idx_file = open('../data/query.idx','w')
for q in queries:
    s = str(idx)
    s = '0'*(4-len(s))+s
    query2id[q] = s
    query_idx_file.write(q+'\t'+s+'\n')
    idx +=1
query_idx_file.close()


rel_file = open('../data/all.qrels','w')
for l in contents:
    query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments = l
    qid = query2id[query]
    docid = '-'.join(['doc',source, qid,rank])
    rel = 'L' + str(int(float(score)))
    rel_file.write(' '.join([qid,docid,rel])+'\n')
rel_file.close()

# res_file = open('../data/all.res','w')
import os
try:
    os.system('rm ../data/SOGOU ../data/HAOSOU ../data/SM ../data/BAIDU')
except:
    print 'no existing result file'
for l in contents:
    # <topicID> <dummy> <documentID> <rank> <docscore> <runname>.
    query, source, url, result_url, type, rank, score, comments, sbs, sbs_comments = l
    qid = query2id[query]
    docid = '-'.join(['doc',source, qid,rank])
    source = source.upper()
    res_file = open('../data/'+source,'a')
    res_file.write(' '.join([query2id[query], 'THUIR',docid,rank,str(int(float(score))),source])+'\n')
    res_file.close()