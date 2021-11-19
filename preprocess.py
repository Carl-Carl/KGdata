import time
import json
from os import system
import tqdm
import numpy as np
import matplotlib.pyplot as plt

'''
[rel2wiki.json] contains all relations and their wiki codes in the dataset
'''

dire = 'data/wiki80/'

def generate_entity_file():
    with open(dire + 'wiki80_val.txt', 'r', encoding='utf8') as data:
        tri = [json.loads(i) for i in data.readlines()]

    v = set()
    for t in tri:
        v.add(t['h']['id'])
        v.add(t['t']['id'])

    x = [a+'\n' for a in v]
    open(dire + 'val_entities.txt', 'w', encoding='utf8').writelines(x)

def generate_triplet_file():
    with open(dire + 'wiki80_train.txt', 'r', encoding='utf8') as data:
        ins = [json.loads(i) for i in data.readlines()]
    with open(dire + 'rel2wiki.json', 'r', encoding='utf8') as data:
        map = json.loads(data.read())

    s = set()
    with open(dire + 'train_triplets.txt', 'w', encoding='utf8') as out:
        for i in ins:
            d = {}
            d['h'] = i['h']['id']
            d['t'] = i['t']['id']
            d['r'] = map[i['relation']]
            id = d['h'] + d['t'] + d['r']
            if id not in s:
                s.add(id)
                json.dump(d, out)
                out.write('\n')
            
        
if __name__ == '__main__':
    generate_entity_file()
    generate_triplet_file()
    
