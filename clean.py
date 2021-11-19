import json

dire = 'data/wiki80/'

with open(dire + 'kg.json', 'r', encoding='utf8') as data:
    tri = [json.loads(i) for i in data.readlines()]

with open(dire + 'train_triplets.txt', 'r', encoding='utf8') as data:
    train = {l.strip() for l in data.readlines()}

with open(dire + 'val_triplets.txt', 'r', encoding='utf8') as data:
    test = {l.strip() for l in data.readlines()}

    
if __name__ == '__main__':
    print('Load  triplets:', len(tri))
    print('Train triplets:', len(train))
    print('Test  triplets:', len(test))
    
    for i in range(len(tri)):
        tri[i].pop('in')
    
    tri = [json.dumps(i) for i in tri]

    tri = set(tri)
    
    tri -= test
    tri |= train
    
    print('Train intersect Test:', len(train.intersection(test)))
    print('Final KG:', len(tri))
    