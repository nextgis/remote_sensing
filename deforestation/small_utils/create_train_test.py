# encoding: utf8

import numpy as np
import pandas as pd


# Функция берет csv файл с выборкой точек
# и возвращает обработанные выборки:
#  - извлечение Path/Row из названий сцен
#  - построчное нормирование выборки
def get_sample(fname):
    # change name 'map1' to 'path_row' 
    names = ['cat', 'poly_cat', 'day', 'path_row', 'map2', 'map3', 'map4', 'map5',
            'x', 'y', 'empty', 'val1', 'val2', 'val3', 'val4', 'val5']
    data = pd.read_csv(fname, delimiter=',', header=None, names=names, usecols=(0, 1, 3, 11, 12, 13, 14, 15),
                         converters={3: lambda x: x[14:20]})
    data['mean'] = data.iloc[:, 3:].apply(np.average, 1)
    
    data['v1'] = data.iloc[:].apply(lambda x: x['val1'] - x['mean'], 1)
    data['v2'] = data.iloc[:].apply(lambda x: x['val2'] - x['mean'], 1)
    data['v3'] = data.iloc[:].apply(lambda x: x['val3'] - x['mean'], 1)
    data['v4'] = data.iloc[:].apply(lambda x: x['val4'] - x['mean'], 1)
    data['v5'] = data.iloc[:].apply(lambda x: x['val5'] - x['mean'], 1)
    
    return data[['cat', 'poly_cat', 'path_row', 'v1', 'v2', 'v3', 'v4', 'v5']]

def get_all_samples(file_list):
    samples = [get_sample(f) for f in file_list]
    return pd.concat(samples)

def reshape_bands(df_list, index_list):
    i = index_list[0]
    result = df_list[0]
    for i in index_list[1:]:
        result = pd.merge(result, df_list[i], on=('cat', 'poly_cat', 'path_row'))
    return result
    
    
# Положительные примеры (вырубки) для каналов 1--5
b1pos = get_all_samples(
    ['data/toar/wint.clean.LC8112027.1.positive', 
      'data/toar/wint.clean.LC8112028.1.positive', 
      'data/toar/wint.clean.LC8113027.1.positive']
)
b2pos = get_all_samples(
    ['data/toar/wint.clean.LC8112027.2.positive', 
      'data/toar/wint.clean.LC8112028.2.positive', 
      'data/toar/wint.clean.LC8113027.2.positive']
)
b3pos = get_all_samples(
    ['data/toar/wint.clean.LC8112027.3.positive', 
      'data/toar/wint.clean.LC8112028.3.positive', 
      'data/toar/wint.clean.LC8113027.3.positive']
)
b4pos = get_all_samples(
    ['data/toar/wint.clean.LC8112027.4.positive', 
      'data/toar/wint.clean.LC8112028.4.positive', 
      'data/toar/wint.clean.LC8113027.4.positive']
)
b5pos = get_all_samples(
    ['data/toar/wint.clean.LC8112027.5.positive', 
      'data/toar/wint.clean.LC8112028.5.positive', 
      'data/toar/wint.clean.LC8113027.5.positive']
)
# b6pos = get_all_samples(
#     ['data/toar/wint.clean.LC8112027.6.positive', 
#       'data/toar/wint.clean.LC8112028.6.positive', 
#       'data/toar/wint.clean.LC8113027.6.positive']
# )
# b7pos = get_all_samples(
#     ['data/toar/wint.clean.LC8112027.7.positive', 
#       'data/toar/wint.clean.LC8112028.7.positive', 
#       'data/toar/wint.clean.LC8113027.7.positive']
# )


# Отрицательные примеры (вырубки отсутствуют) для каналов 1--5
b1neg = get_all_samples(
    ['data/toar/wint.clean.LC8112027.1.negative', 
      'data/toar/wint.clean.LC8112028.1.negative', 
      'data/toar/wint.clean.LC8113027.1.negative']
)
b2neg = get_all_samples(
    ['data/toar/wint.clean.LC8112027.2.negative', 
      'data/toar/wint.clean.LC8112028.2.negative', 
      'data/toar/wint.clean.LC8113027.2.negative']
)
b3neg = get_all_samples(
    ['data/toar/wint.clean.LC8112027.3.negative', 
      'data/toar/wint.clean.LC8112028.3.negative', 
      'data/toar/wint.clean.LC8113027.3.negative']
)
b4neg = get_all_samples(
    ['data/toar/wint.clean.LC8112027.4.negative', 
      'data/toar/wint.clean.LC8112028.4.negative', 
      'data/toar/wint.clean.LC8113027.4.negative']
)
b5neg = get_all_samples(
    ['data/toar/wint.clean.LC8112027.5.negative', 
      'data/toar/wint.clean.LC8112028.5.negative', 
      'data/toar/wint.clean.LC8113027.5.negative']
)
# b6neg = get_all_samples(
#     ['data/toar/wint.clean.LC8112027.6.negative', 
#       'data/toar/wint.clean.LC8112028.6.negative', 
#       'data/toar/wint.clean.LC8113027.6.negative']
# )
# b7neg = get_all_samples(
#     ['data/toar/wint.clean.LC8112027.7.negative', 
#       'data/toar/wint.clean.LC8112028.7.negative', 
#       'data/toar/wint.clean.LC8113027.7.negative']
# )


pos = reshape_bands([b1pos, b2pos, b3pos, b4pos, b5pos], [0, 1, 2, 3, 4])
pos['y'] = 1

neg = reshape_bands([b1neg, b2neg, b3neg, b4neg, b5neg], [0, 1, 2, 3, 4])
neg['y'] = 0

val_train_ratio = 0.25

poly_pcat = pos.poly_cat.unique()
lenp = len(poly_pcat)
valp_cat = np.random.choice(poly_pcat, int(val_train_ratio*lenp))

valp = pos[pos.poly_cat.isin(valp_cat)]
trainp = pos[~pos.poly_cat.isin(valp)]

poly_ncat = neg.poly_cat.unique()
lenn = len(poly_ncat)
valn_cat = np.random.choice(poly_ncat, int(val_train_ratio*lenn))

valn = neg[neg.poly_cat.isin(valn_cat)]
trainn = neg[~neg.poly_cat.isin(valn)]

train_data = pd.concat([trainp, trainn], ignore_index=True)
train_data = train_data.reindex(np.random.permutation(train_data.index)) 
val_data = pd.concat([valp, valn], ignore_index=True)
val_data = val_data.reindex(np.random.permutation(val_data.index)) 


training_data = train_data.iloc[:, 3:29]

valid_data = val_data.iloc[:, 3:29]

training_data.to_csv('data/toar/train.csv', sep=",", index=False, header=False)
valid_data.to_csv('data/toar/val.csv', sep=",", index=False, header=False) 
