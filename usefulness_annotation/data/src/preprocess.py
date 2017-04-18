__author__ = 'franky'

from collections import defaultdict


def task_to_sessions():
    task_to_sessions_dict = defaultdict(lambda: set())
    fin = open("../../temp/annotation_sequence.tsv").readlines()[1:]
    for line in fin:
        id,session_id,user_id,setting_id,task_id,source_id,annotation_index,result_id,timestamp,is_clicked,click_dwell_time,clicked_url,weighted_exposed_time = line.strip().split('\t')
        task_to_sessions_dict[task_id].add(session_id)
    return task_to_sessions_dict


task_to_sessions_dict = task_to_sessions()
tasks = []
for i in range(2, 21):
    tasks.append(str(i))

usefulnesses = defaultdict(lambda: defaultdict(lambda: {}))
fin = open("../anno_usefulness.csv").readlines()[1:]
for line in fin:
    _,assessor_id,session_id,index,score = line.strip().split(',')
    usefulnesses[session_id][index][assessor_id] = score

for task in tasks:
    sessions = task_to_sessions_dict[task]
    for session in sessions:
        for index in usefulnesses[session].keys():
            if len(usefulnesses[session][index]) != 3:
                print 'use', task, session, index, usefulnesses[session][index]

satisfactions = defaultdict(lambda: {})
fin = open("../anno_tasksatisfaction.csv").readlines()[1:]
for line in fin:
    id,assessor_id,session_id,score = line.strip().split(',')
    satisfactions[session_id][assessor_id] = score

for task in tasks:
    sessions = task_to_sessions_dict[task]
    for session in sessions:
        if len(satisfactions[session]) != 3:
            print 'sat', task, session, satisfactions[session]
