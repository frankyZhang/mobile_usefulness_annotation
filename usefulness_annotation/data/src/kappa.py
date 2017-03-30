__author__ = 'franky'

from sklearn.metrics import cohen_kappa_score
from collections import defaultdict
import numpy as np


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
    fout = open("../anno_usefulness.csv").readlines()[1:]
    for line in fout:
        id,assessor_id,session_id,index,score = line.strip().split(',')
        usefulnesses[session_id][index][assessor_id] = score
        '''if int(score) > 2:
            usefulnesses[session_id][index][assessor_id] = 1
        else:
            usefulnesses[session_id][index][assessor_id] = 0'''
    annotations = defaultdict(lambda: [])
    for session_id in usefulnesses.keys():
        for index in usefulnesses[session_id].keys():
            for assessor_id in usefulnesses[session_id][index].keys():
                annotations[assessor_id].append(usefulnesses[session_id][index][assessor_id])

    for i in range(len(annotations.keys())):
        for j in range(i+1, len(annotations.keys())):

    #items.append(cohen_kappa_score(annotation_i, annotation_j, ['1','2','3','4']))
    #items.append(cohen_kappa_score(annotation_i, annotation_j, [0,1]))
            print 'usefulness cohen', annotations.keys()[i], annotations.keys()[j], cohen_kappa_score(annotations[annotations.keys()[i]], annotations[annotations.keys()[j]], ['1','2','3','4'])
            #print 'usefulness cohen', annotations.keys()[i], annotations.keys()[j], cohen_kappa_score(annotations[annotations.keys()[i]], annotations[annotations.keys()[j]], [0, 1])
    #print np.mean(items)


def usefulness_fleiss_kappa():
    usefulnesses = defaultdict(lambda: defaultdict(lambda: {}))
    fout = open("../anno_usefulness.csv").readlines()[1:]
    assessors = set()
    for line in fout:
        id,assessor_id,session_id,index,score = line.strip().split(',')
        usefulnesses[session_id][index][assessor_id] = int(score)
        assessors.add(assessor_id)
    assessors_list = []
    for assessor in assessors:
        assessors_list.append(assessor)
    annotations_table = []

    sub_num = 0
    for session_id in usefulnesses.keys():
        for index in usefulnesses[session_id].keys():
            sub_num += 1

    annotations_array = np.zeros((sub_num, 4))
    i = 0
    for session_id in usefulnesses.keys():
        for index in usefulnesses[session_id].keys():
            for assessor in assessors_list:
                annotations_array[i][usefulnesses[session_id][index][assessor]-1] += 1
            i += 1

    #print np.matrix(annotations_table)
    print 'usefulness fleiss', fleiss_kappa(annotations_array)


def satisfaction_kappa():
    items = []
    satisfactions = defaultdict(lambda: {})
    fout = open("../anno_tasksatisfaction.csv").readlines()[1:]
    for line in fout:
        id,assessor_id,session_id,score = line.strip().split(',')
        satisfactions[session_id][assessor_id] = score
        '''if int(score) > 4:
            satisfactions[session_id][assessor_id] = 1
        else:
            satisfactions[session_id][assessor_id] = 0'''
    annotations = defaultdict(lambda: [])
    for session_id in satisfactions.keys():
        for assessor_id in satisfactions[session_id].keys():
            annotations[assessor_id].append(satisfactions[session_id][assessor_id])

    for i in range(len(annotations.keys())):
        for j in range(i+1, len(annotations.keys())):

    #items.append(cohen_kappa_score(annotation_i, annotation_j, ['1','2','3','4','5']))
    #items.append(cohen_kappa_score(annotation_i, annotation_j, [0,1]))
            print 'satisfaction cohen', annotations.keys()[i], annotations.keys()[j], cohen_kappa_score(annotations[annotations.keys()[i]], annotations[annotations.keys()[j]], ['1','2','3','4','5'])
            #print 'satisfaction', annotations.keys()[i], annotations.keys()[j], cohen_kappa_score(annotations[annotations.keys()[i]], annotations[annotations.keys()[j]], [0, 1])
    #print np.mean(items)


def satisfactioin_fleiss_kappa():
    satisfactions = defaultdict(lambda: {})
    fout = open("../anno_tasksatisfaction.csv").readlines()[1:]
    assessors = set()
    for line in fout:
        id,assessor_id,session_id,score = line.strip().split(',')
        satisfactions[session_id][assessor_id] = int(score)
        assessors.add(assessor_id)
    assessors_list = []
    for assessor in assessors:
        assessors_list.append(assessor)
    annotations_table = []

    annotations_array = np.zeros((43, 5))
    i = 0
    for session_id in satisfactions.keys():
        for assessor in assessors_list:
            annotations_array[i][satisfactions[session_id][assessor]-1] += 1
        i += 1

    #print np.matrix(annotations_table)
    print 'satisfaction fleiss', fleiss_kappa(annotations_array)


if __name__ == "__main__":
    usefulness_kappa()
    usefulness_fleiss_kappa()
    satisfaction_kappa()
    satisfactioin_fleiss_kappa()
