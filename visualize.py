import json
import tqdm
import numpy as np
import matplotlib.pyplot as plt

def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            plt.annotate('{:.2f}%'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height*0.99),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2,height,height, ha='center', va='bottom')
        rect.set_edgecolor('white')
        
def draw(a, string, dire):
    a = np.array(a, float) 

    a /= a.sum()/100

    a.round(2, a)

    r = plt.bar(range(len(a)), a, width=0.8, label=string)
    autolabel(r)
    plt.legend(loc='best')
    # add_labels(r)
    plt.savefig(dire + string[:-3] + '.png')
    plt.close()
    

dire = 'data/wiki80/'

data = open(dire + 'kg1.json', 'r', encoding='utf8').readlines()
tri = [json.loads(i) for i in data]

with open(dire + 'train_entities.txt', 'r', encoding='utf8') as data:
    e_set = {l.strip() for l in data.readlines()}

with open(dire + 'val_entities.txt', 'r', encoding='utf8') as data:
    e_set = e_set.union({l.strip() for l in data.readlines()})

if __name__ == '__main__':
    d = {}
    for i in e_set:
        d[i] = 0
        
    knw = [0]*11
    unk = [0]*11

    t_t = 0
    for t in tri:
        # if t['in'] == 'T':
            if t['h'] not in d:
                print(t['h'], 'not found')
            else:
                d[t['h']] += 1
                t_t += 1

    
    for i in d.values():
        knw[min(i, 10)] += 1

    # for t in tri:
    #     if t['in'] == 'F':
    #         if t['h'] not in d:
    #             print(t['h'], 'not found')
    #         else:
    #             d[t['h']] += 1

    # for i in d.values():
    #     unk[i] += 1
    
    print('Known count:\n' + str(knw))
    print('All count:\n' + str(unk))
    # if sum(knw) != sum(unk):
    #     print('Sum error.')
    #     print(sum(knw), sum(unk))
    #     exit()
    print('Total entities :', sum(knw))
    print('In-set triplets:', t_t)
    print('Total triplets :', len(tri))
    
    draw(knw, 'Proportions of in-set triplets: %', dire)
    # draw(unk, 'Proportions of all triplets: %', dire)

