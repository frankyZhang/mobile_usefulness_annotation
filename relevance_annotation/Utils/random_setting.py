__author__ = 'franky'
import random


def random_setting(filename):
    f = open(filename, 'w')
    col = []
    for j in range(20):
        col.append({1: 0, 2: 0, 3: 0, 4: 0})
    for i in range(40):
        source_list = []
        row = {1: 0, 2: 0, 3: 0, 4: 0}
        for j in range(20):
            choices = [1, 2, 3, 4]
            while True:
                print choices
                source_id = choices[random.randint(0, len(choices)-1)]
                print row[source_id], col[j][source_id]
                if row[source_id] < 5 and col[j][source_id] < 10:
                    row[source_id] += 1
                    col[j][source_id] += 1
                    source_list.append(source_id)
                    break
                else:
                    choices.remove(source_id)
        f.write(','.join(str(item) for item in source_list))
        f.write('\n')
    f.close()


if __name__ == "__main__":
    random_setting("../temp/setting.csv")
