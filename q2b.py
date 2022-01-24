from numpy.core.defchararray import add
import pandas as pd
import numpy as np
from pandas.io.formats.format import set_eng_float_format

inputs = pd.read_csv('inputs.csv')
output = pd.read_csv('outputs.csv')
tags = pd.read_csv('tags.csv')
transactions = pd.read_csv('transactions.csv')

def clusterfun(inputs,key):
    locate = inputs.loc[inputs['sig_id']==key]
    if(locate.empty):
        return []
    inputs = inputs.loc[inputs['tx_id'].isin(locate['tx_id'])]
    return inputs.sig_id

def unspent(output, cluster):
    if(len(cluster)==0):
        return -1
    output = output.loc[output['pk_id'].isin(cluster)]
    return output.value.sum()

used = output[output['id'].isin(inputs['output_id'])]
UTXO = pd.concat([output,used]).drop_duplicates(keep=False)

cluster = UTXO.loc[UTXO['pk_id'].isin(tags['pk_id'])]
print(cluster)
#according to UTXO, we can find 164412 has unpsent bitcoins
cluster = output.loc[output['pk_id'].isin(tags['pk_id'])]
print(cluster)
cluster =inputs.loc[inputs['sig_id'].isin(tags['pk_id'])]
print(cluster)

Exchange = tags.loc[tags['type']=='Exchange']
DarkMarket = tags.loc[tags['type']=='DarkMarket']
Vendor = tags.loc[tags['type']=='Vendor']
Wallet = tags.loc[tags['type']=='Wallet']


id = 0
value = 0
s =[]
#find cluster for every pk_id
for i in tags.pk_id:
    a = unspent(UTXO,clusterfun(inputs,i))
    if a == -1:
        a = UTXO.loc[UTXO['pk_id']==i].value
    s.append(a)
    print(i)
    print(a)
tags.insert(loc=len(tags.columns),column='UTXO',value=s)
print("ffffff")
#print(UTXO.loc[UTXO['pk_id']==24644].value)
print(tags)
# 31846
# 55451000000
# 164412
# 1000000000000
# 42423
# 5099000000
# 157666
# 1880000000000 (最大)
# 71159
# 1000000000000
# the name PeakNevis has the most bitcoins, pk_id 157666 , 
exchanges = tags.loc[tags['name']=='PeakNevis'].UTXO.sum()
print(exchanges)
#3885099000000

#find clusters from pk_id in exchange, check all inputs
#compare the same tx_id and sum up
keylist = []
for i in Exchange.pk_id:
    keylist = np.append(keylist,clusterfun(inputs,i))
print(keylist)
target = inputs.loc[inputs['sig_id'].isin(keylist)]
print(target)
list1 = []
for i in DarkMarket.pk_id:
    list1 = np.append(list1,clusterfun(inputs,i))
print(list1)
locate =output.loc[output['pk_id'].isin(list1)]
print(locate)
##
x = target.tx_id
y = locate.tx_id
c=list(set(x).intersection(set(y)))
print('ggggggg')
print(len(c))
print(output.loc[output['tx_id'].isin(c)].value.sum())

intersected = pd.merge(target,locate, on=['tx_id'],how='inner')
print(intersected)
print(intersected.tx_id.unique())
#[ 57450  57746  59456  59618  86621 104152 111248]
print(output.loc[output['tx_id'].isin(intersected.tx_id)])
print(output.loc[output['tx_id'].isin(intersected.tx_id)].value.sum())
# the result is 1870000000000
