__author__ = 'franky'

from sklearn.metrics import cohen_kappa_score
from collections import defaultdict
import numpy as np


assessor_groups = [
    ['2016211001', '2013011392', '2013012195'],
    ['2014011426', '2014011325', '2016011258']
]


def task_to_sessions():
    task_to_sessions_dict = defaultdict(lambda: set())
    fin = open("../../temp/annotation_sequence.tsv").readlines()[1:]
    for line in fin:
        id,session_id,user_id,setting_id,task_id,source_id,annotation_index,result_id,timestamp,is_clicked,click_dwell_time,clicked_url,weighted_exposed_time = line.strip().split('\t')
        task_to_sessions_dict[task_id].add(session_id)
    return task_to_sessions_dict


task_to_sessions_dict = task_to_sessions()
tasks = []
for i in range(1, 3):
    if i != 17:
        tasks.append(str(i))


def fleiss_kappa(table):
    '''Fleiss' kappa multi-rater agreement measure

    Parameters
    ----------
    table : array_like, 2-D
        assumes subjects in rows, and categories in columns

    Returns
    -------
    kappa : float
        Fleiss's kappa statistic for inter rater agreement

    Notes
    -----
    coded from Wikipedia page
    http://en.wikipedia.org/wiki/Fleiss%27_kappa

    no variance or tests yet

    '''
    table = 1.0 * np.asarray(table)   #avoid integer division
    n_sub, n_cat = table.shape
    n_total = table.sum()
    n_rater = table.sum(1)
    n_rat = n_rater.max()
    #assume fully ranked
    assert n_total == n_sub * n_rat

    #marginal frequency  of categories
    p_cat = table.sum(0) / n_total

    table2 = table * table
    p_rat = (table2.sum(1) - n_rat) / (n_rat * (n_rat - 1.))
    p_mean = p_rat.mean()

    p_mean_exp = (p_cat*p_cat).sum()

    kappa = (p_mean - p_mean_exp) / (1 - p_mean_exp)
    return kappa


def usefulness_kappa():
    items = []
    usefulnesses = defaultdict(lambda: defaultdict(lambda: {}))
    fin = open("../anno_usefulness.csv").readlines()[1:]
    for line in fin:
        id,assessor_id,session_id,index,score = line.strip().split(',')
        usefulnesses[session_id][index][assessor_id] = score
        '''if int(score) > 2:
            usefulnesses[session_id][index][assessor_id] = 1
        else:
            usefulnesses[session_id][index][assessor_id] = 0'''
    for task in tasks:
        assessors_annotations = defaultdict(lambda: [])
        for session_id in task_to_sessions_dict[task]:
            for index in usefulnesses[session_id].keys():
                for assessor_id in usefulnesses[session_id][index].keys():
                    assessors_annotations[assessor_id].append(usefulnesses[session_id][index][assessor_id])

        for i in range(len(assessors_annotations.keys())):
            for j in range(i+1, len(assessors_annotations.keys())):
                assessor_i = assessors_annotations.keys()[i]
                assessor_j = assessors_annotations.keys()[j]
                if len(assessors_annotations[assessor_i]) == len(assessors_annotations[assessor_j]):
            #items.append(cohen_kappa_score(annotation_i, annotation_j, ['1','2','3','4']))
            #items.append(cohen_kappa_score(annotation_i, annotation_j, [0,1]))
                    print 'task:'+task, '\tusefulness cohen:', assessor_i, assessor_j, cohen_kappa_score(assessors_annotations[assessor_i], assessors_annotations[assessor_j], ['1','2','3','4'])
                    #print 'usefulness cohen', annotations.keys()[i], annotations.keys()[j], cohen_kappa_score(annotations[annotations.keys()[i]], annotations[annotations.keys()[j]], [0, 1])
            #print np.mean(items)


def usefulness_fleiss_kappa():
    usefulnesses = defaultdict(lambda: defaultdict(lambda: {}))
    fin = open("../anno_usefulness.csv").readlines()[1:]
    assessors = set()
    for line in fin:
        id,assessor_id,session_id,index,score = line.strip().split(',')
        usefulnesses[session_id][index][assessor_id] = int(score)
        assessors.add(assessor_id)
    assessors_list = []
    for assessor in assessors:
        assessors_list.append(assessor)
    annotations_table = []

    for task in tasks:
        sub_num = 0
        for session_id in task_to_sessions_dict[task]:
            for index in usefulnesses[session_id].keys():
                sub_num += 1

        annotations_array = np.zeros((sub_num, 4))
        i = 0
        for session_id in task_to_sessions_dict[task]:
            for index in usefulnesses[session_id].keys():
                for assessor in usefulnesses[session_id][index].keys():
                    annotations_array[i][usefulnesses[session_id][index][assessor]-1] += 1
                i += 1

        #print np.matrix(annotations_table)
        print 'task:'+task, '\tusefulness fleiss:', fleiss_kappa(annotations_array)


def satisfaction_kappa():
    items = []
    satisfactions = defaultdict(lambda: {})
    fin = open("../anno_tasksatisfaction.csv").readlines()[1:]
    for line in fin:
        id,assessor_id,session_id,score = line.strip().split(',')
        satisfactions[session_id][assessor_id] = score
        '''if int(score) > 4:
            satisfactions[session_id][assessor_id] = 1
        else:
            satisfactions[session_id][assessor_id] = 0'''

    for task in tasks:
        assessors_annotations = defaultdict(lambda: [])
        for session_id in task_to_sessions_dict[task]:
            for assessor_id in satisfactions[session_id].keys():
                assessors_annotations[assessor_id].append(satisfactions[session_id][assessor_id])

        for i in range(len(assessors_annotations.keys())):
            for j in range(i+1, len(assessors_annotations.keys())):
                assessor_i = assessors_annotations.keys()[i]
                assessor_j = assessors_annotations.keys()[j]
                if len(assessors_annotations[assessor_i]) == len(assessors_annotations[assessor_j]):
        #items.append(cohen_kappa_score(annotation_i, annotation_j, ['1','2','3','4','5']))
        #items.append(cohen_kappa_score(annotation_i, annotation_j, [0,1]))
                    print 'task:'+task, '\tsatisfaction cohen', assessor_i, assessor_j, cohen_kappa_score(assessors_annotations[assessor_i], assessors_annotations[assessor_j], ['1','2','3','4','5'])
                #print 'satisfaction', annotations.keys()[i], annotations.keys()[j], cohen_kappa_score(annotations[annotations.keys()[i]], annotations[annotations.keys()[j]], [0, 1])
        #print np.mean(items)


def satisfactioin_fleiss_kappa():
    satisfactions = defaultdict(lambda: {})
    fin = open("../anno_tasksatisfaction.csv").readlines()[1:]
    assessors = set()
    for line in fin:
        id,assessor_id,session_id,score = line.strip().split(',')
        satisfactions[session_id][assessor_id] = int(score)
        assessors.add(assessor_id)
    assessors_list = []
    for assessor in assessors:
        assessors_list.append(assessor)
    annotations_table = []

    for task in tasks:
        annotations_array = np.zeros((43, 5))
        i = 0
        for session_id in task_to_sessions_dict[task]:
            for assessor in satisfactions[session_id].keys():
                annotations_array[i][satisfactions[session_id][assessor]-1] += 1
            i += 1

        #print np.matrix(annotations_table)
        print 'task:'+task, '\tsatisfaction fleiss', fleiss_kappa(annotations_array)


if __name__ == "__main__":
    usefulness_kappa()
    usefulness_fleiss_kappa()
    satisfaction_kappa()
    satisfactioin_fleiss_kappa()
