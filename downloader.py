
import atexit
import os
import time
import requests
import json
from tqdm import tqdm
import visualize

dire = 'data/wiki80/'
last_entity = 0
TRIPLET_MAX = 10
log = open(dire + 'download.txt', 'a', encoding='utf8')


def get_entities():
    '''
        return:
        e_set: All entities.
        entity: Entities to download in groups.
    '''
    with open(dire + 'train_entities.txt', 'r', encoding='utf8') as data:
        e_set = {l.strip() for l in data.readlines()}
    
    with open(dire + 'val_entities.txt', 'r', encoding='utf8') as data:
        e_set = e_set.union({l.strip() for l in data.readlines()})
    
    temp_list = list(e_set)
    temp_list.sort()
    
    finish = open(dire + 'download.txt', 'r', encoding='utf8').readlines()

    if len(finish) != 0 and finish[1] == 'not finish\n':
        global last_entity
        last_entity = int(finish[0])
        temp_list = temp_list[last_entity:]
        with open(dire + 'download.txt', 'w', encoding='utf8') as f:
            pass
        
    entity = []
    i = 0
    l = 50
    while i < len(temp_list):
        entity.append(temp_list[i:min(i+l, len(temp_list))])
        i += l
    return e_set, entity

 
@atexit.register
def exit_depose():
    global last_entity, log
    log.write(str(last_entity) + '\nnot finish\n')
    log.close()
    print('Not finish.')


if __name__ == '__main__':
    entity_set, entity_slice = get_entities()
            
    for head in tqdm(entity_slice):
        # connect to host
        stop = 0
        while True:
            try:
                files = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='
                                + '|'.join(head) 
                                + '&format=json&languages=en').json()['entities']
                t1 = set(head)
                t2 = set(files.keys())
                if t1 == t2:
                    break
            except:
                print('\nwaiting for response.')
                time.sleep(3)
            if stop >= 5:
                exit('0')
            stop += 1

        f = open(dire + 'temp/' + str(last_entity) + '.json', 'w', encoding='utf8')
        try:
            f.write(json.dumps(files))
            f.close()
        except:
            f.close()
            last_entity += 50
            exit('')
            
        last_entity += 50
            
        
