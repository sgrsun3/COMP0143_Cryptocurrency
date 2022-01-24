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
        return 0
    #根据cluster 查到有多少value
    output = output.loc[output['pk_id'].isin(cluster)]
    return output.value.sum()
    #print(output)
    #output = output.sum()
    #查看有哪些给了别的pk，哪些留给了自己，找到output，根据outputid找到input里面有哪些用了
    # associate = inputs.loc[inputs['output_id'].isin(output['id'])]
    #print(associate)
    #变成空的,这里写错啦
    # output = pd.read_csv('outputs.csv')
    # associate = output.loc[output['tx_id'].isin(associate['tx_id'])]
    #print(associate)
    #如果是给了自己，output上面记录的pk_id肯定是自己的,
    # change = associate.loc[associate['pk_id'].isin(cluster)]
    # return change['value'].sum()
# x = cluster(inputs,89688)
# print(unspent(output,x))
print('aaaaaaa')
x = clusterfun(inputs,41442)
y = list(set(x))
print(len(y)) #50
print(np.sort(y)) # 40248, 41911
# print(unspent(output,x))
#对input去重每个tx_id 应用的sigid 要保证独一无二
inputsunique = inputs.drop_duplicates(subset=["tx_id","sig_id"],keep='first')
x = pd.value_counts(inputsunique["tx_id"])
print(x)
#121713, 140484
cluster = inputs.loc[inputs['tx_id']==121713]
cluster = cluster.sig_id.unique()
print(cluster.size)
print(np.sort(cluster))
#print(cluster.sort_values(by="sig_id",ascending=False))
#b, 最大的是89688 最小的是2172, 901个



#先算出UTXO 列出来
used = output[output['id'].isin(inputs['output_id'])]
UTXO = pd.concat([output,used]).drop_duplicates(keep=False)
owner = inputs[inputs['tx_id'].isin(UTXO['tx_id'])]
#owner 中的sig_id 如果和output中的pk_id 相同说明是自己的
print(UTXO.sort_values(by="value",ascending=False))
# print(UTXO.groupby('pk_id').value.sum())
# tx_id:140479 value:9000000000000
# 共有71080个UTXO, 每个属于不同的key
new = UTXO.groupby('tx_id').value.sum()
print(new.sort_values())
print(new.size)

# tx_id:140479 sig_id = 138871, value:9000000000000 according to the output, output_id = 170400
clusters = inputs.loc[inputs['tx_id']==140479]
print(clusters)
# tx_id: 140479 pk_id 138895
local = output.loc[output['tx_id']==140479]
print(local)
test = output.loc[output['id']==170400]
print(test)
# we find that tx_id 140455, 

new2 = UTXO.groupby('pk_id').value.sum()
print(new2.sort_values())
print(new2.size)
#length = 65346
#138895    9000000000000
#745       7237436000000
#150171    5790065000000
#152715    5000000000000
#121636    4000000000000
clusters = inputs.loc[inputs['sig_id']==138895]
print(clusters)
clusters = inputs.loc[inputs['sig_id']==745]
print(clusters)
clusters = inputs.loc[inputs['sig_id']==150171]
print(clusters)
clusters = inputs.loc[inputs['sig_id']==152715]
print(clusters)
clusters = inputs.loc[inputs['sig_id']==121636]
print(clusters)
# 如果为空说明cluster 只有自己
print(unspent(UTXO,clusterfun(inputs,152715)))
print(unspent(UTXO,clusterfun(inputs,121636)))
#3题答案
#find the key asscoiated with inputs
id = 0
value = 0
for i in new2.index:
    a = unspent(UTXO,clusterfun(inputs,i))
    if (a>value):
        value = a
        id=i
        print(value)
        print(i)

#c. 4755624000000, 38498 c不一样
#d.
locate = inputs.loc[inputs['sig_id']==38498]
inputs = inputs.loc[inputs['tx_id'].isin(locate['tx_id'])]
print(inputs)
#the cluster pk_id: 38498，39508，39508，37214，37299
tx1 = output.loc[output['id']==41613]
print(tx1)
tx1 = output.loc[output['id']==42267]
print(tx1)
tx1 = output.loc[output['id']==43930]
print(tx1)
tx1 = output.loc[output['id']==37431]
print(tx1)
tx1 = output.loc[output['id']==37518]
print(tx1)
##(d)
value =UTXO.loc[UTXO['pk_id'].isin([38498,39508,39508,37214,37299])]
print(value)
print(value.value.sum())
## tx_id 38632, pk_id 38498, value = 1186780000000

