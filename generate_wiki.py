
import os
import time
import json
from tqdm import tqdm

dire = 'data/wiki80/'
TRIPLET_MAX = 10

def get_entities():
    with open(dire + 'train_entities.txt', 'r', encoding='utf8') as data:
        e_set = {l.strip() for l in data.readlines()}
    
    with open(dire + 'val_entities.txt', 'r', encoding='utf8') as data:
        e_set = e_set.union({l.strip() for l in data.readlines()})

    return e_set

if __name__ == '__main__':
    entity_set = get_entities()
    
    log = open(dire + 'entity_not_found.txt', 'w', encoding='utf8')
    with open(dire + 'wiki2rel.json', 'r', encoding='utf8') as data:
        r_set = json.loads(data.read())

    with open(dire + 'kg.json', 'w', encoding='utf8') as f:
        dir = os.listdir(dire + '/temp')
        for doc in tqdm(dir):
            with open(dire + '/temp/' + doc, 'r') as c:
                files = json.loads(c.read())
            
            '''
                get in:T triplets
            '''
            for head_id, file in files.items():
                if not file.get('claims'):
                    log.write(head_id + '\n')
                    log.flush()
                    continue
                
                file = file['claims']
                cnt = 0
                
                # all known relations
                for relation in r_set:
                    if file.get(relation) and \
                        file[relation][0]['mainsnak']['datatype'] == 'wikibase-item':
                            
                        for t in file[relation]:
                            try:
                                triplet = {}
                                tail = t['mainsnak']['datavalue']
                                if tail['type'] == 'wikibase-entityid' and \
                                    tail['value']['id'] in entity_set:
                                        
                                    triplet['h'] = head_id
                                    triplet['t'] = tail['value']['id']
                                    triplet['r'] = relation
                                    triplet['in'] = 'T'
                                    f.write(json.dumps(triplet) + '\n')
                                    f.flush()
                                    cnt += 1
                                    if cnt >= TRIPLET_MAX:
                                        break
                            except KeyError:
                                continue
                        if cnt >= TRIPLET_MAX:
                                break
                
                
                # if cnt >= TRIPLET_MAX:
                #     continue
                
                '''
                    get in:F triplets
                '''
                # for r, v in file.items():
                #     for t in v:
                #         if not t['mainsnak']['datatype'] == 'wikibase-item':
                #             continue
                    
                #         try:
                #             triplet = {}
                #             tail = t['mainsnak']['datavalue']
                #             if tail['type'] == 'wikibase-entityid' and \
                #                 (tail['value']['id'] not in entity_set or r not in r_set):
                #                 triplet['h'] = head_id
                #                 triplet['t'] = tail['value']['id']
                #                 triplet['r'] = r
                #                 triplet['in'] = 'F'
                #                 f.write(json.dumps(triplet) + '\n')
                #                 f.flush()
                                
                #                 cnt += 1
                #                 if cnt >= TRIPLET_MAX:
                #                     break
                #         except KeyError:
                #             continue
                        
                #     if cnt >= TRIPLET_MAX:
                #         break

        
