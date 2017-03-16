#coding=utf8
import sys
from openpyxl import load_workbook
def load_content():

    wb2 = load_workbook('../docs/top5_50_0919.xlsx')
    sheet1 = wb2.get_sheet_by_name(u'top5')
    contents = []
    for r in range(2, 1002, 1):
        line = []
        for c in 'ABCDEFGHIJKLM':
            if c == 'C':
                try:
                    val = sheet1[c + str(r)].hyperlink.display
                except:
                    val = ''
            else:
                val = str(sheet1[c + str(r)].value)
            line.append(val)
        contents.append(line)
    return contents

def load_query2id():
    query2id = dict()
    for l in open('../data/query.idx'):
        segs = l.strip().split('\t')
        query, id = segs
        query2id[query] = id
    return query2id

def load_id2query():
    id2query = dict()
    for l in open('../data/query.idx'):
        segs = l.strip().split('\t')
        query, id = segs
        id2query[id] = query
    return id2query




