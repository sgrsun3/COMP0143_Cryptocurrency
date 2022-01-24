import pandas as pd

# Question A
# Question a
qa_txnum = pd.read_csv('transactions.csv', usecols=['id'])
print("Answer a (total transactions) is: ", len(qa_txnum))
print("")
print("==================================End of Answer=================================================")

# Question b
input_df = pd.read_csv('inputs.csv', usecols=['id', 'tx_id'])
output_df = pd.read_csv('outputs.csv', usecols=['id', 'tx_id'])
input_id = set()
output_id = set()
tx_id_count = -1
listtt = []

# create an empty set
# if the value appears only once, add it to the empty set
for i in input_df['tx_id'].values:
    if i not in input_id and tx_id_count != i:
        input_id.add(i)
    elif i in input_id:
        input_id.remove(i)
    tx_id_count = i
# print(len(input_set))

for j in output_df['tx_id'].values:
       if tx_id_count != j:
           listtt.clear()
           listtt.append(j)
       else:
           listtt.append(j)
       if j not in output_id:
           output_id.add(j)
       if listtt.count(j) != 1:
           output_id.remove(j)
       tx_id_count = j
# print(len(output_set))

# the joint part of two sets is the same transaction
intersection = input_id.intersection(output_id)
print("Answer b (1 input 1 output) is: ", len(intersection))
print("")
print("==================================End of Answer=================================================")

# Question c
new_set = set()
# create a new list, stores tx_id in the list
# if the count of tx_id is not 2, then remove it from the set
listt = []
for k in output_df['tx_id'].values:
       if tx_id_count != k:
           listt.clear()
           listt.append(k)
       else:
           listt.append(k)
       if k not in new_set:
           new_set.add(k)
       if listt.count(k) != 2:
           new_set.remove(k)
       tx_id_count = k
intersection1 = input_id.intersection(new_set)
print("Answer c (1 input 2 outputs) is: ",len(intersection1))
print("")
print("==================================End of Answer=================================================")

# Question d
qd_outputs = pd.read_csv('outputs.csv')
qd_inputs = pd.read_csv('inputs.csv')
total_num = len(qd_outputs['value'])
# print(total_num)
used_num = len(qd_outputs[qd_outputs['id'].isin(qd_inputs['output_id'])])
# utxo = total number - used coins
UTXO_num = total_num - used_num
print("Answer d (total UTXOs) is: ", UTXO_num)
print("")
print("==================================End of Answer=================================================")

# Question e
qe = pd.read_csv('outputs.csv')
output_max = qe.loc[qe['value'] == qe['value'].max()]
print("Answer e (the highest associated value output ids) is: ", output_max['id'])
print("")
print("==================================End of Answer=================================================")

# Question f
qf = pd.read_csv('outputs.csv', usecols=['pk_id'])
# remove the duplicated pk
qf = qf.drop_duplicates()
d_pk = qf.loc[qf['pk_id'] != -10]
print("Answer f (distinct public keys used across all blocks) is: ", len(d_pk))
print("")
print("==================================End of Answer=================================================")

# Question g
qg = pd.read_csv('outputs.csv')
pk = qg.loc[qg['value'] == qg['value'].max()]
print("Answer g (the public key id received the highest number of bitcoins) is: ", pk['pk_id'])
v_max = qg['value'].max()
bit_num = v_max * 0.00000001
print("Answer g (the highest number of bitcoins) is: ", bit_num)
print("")
print("==================================End of Answer=================================================")

# Question h
qh = pd.read_csv('outputs.csv')
qh = qh['pk_id'].value_counts()
max_num = qh.max()
print("Answer h (max number of times output id) is: ", qh.index[0])
# the first element is public key id according to 'value_counts()'
print("Answer h (the most number of times) is: ", max_num)
print("")
print("==================================End of Answer=================================================")

# Question i
inputs = pd.read_csv('inputs.csv')
outputs = pd.read_csv('outputs.csv')
tags = pd.read_csv('tags.csv')
transactions = pd.read_csv('transactions.csv')

outputs_data = outputs
outputs_data.rename(columns ={'id':'output_id'}, inplace = True)

# Invalid 1: The transaction uses the UTXO which does not belong to its address
# id  tx_id_x  sig_id  output_id  tx_id_y   pk_id       value
# 194075   138278  139250      16121    16081   16020  5000000000
merge = pd.merge(inputs,outputs_data, on = 'output_id').dropna()
invalid1 = merge.loc[merge['sig_id'] != merge['pk_id']]
print(invalid1)

# Invalid 2: unequal input value and output value
# tx_id       value_x       value_y
# 2863      3493000000    3393000000
# 2864      3393000000    3293000000
merge1 = pd.merge(inputs,outputs_data[['output_id','value']], on = 'output_id')
inputs_value = merge1[['tx_id','value']].groupby('tx_id').sum()
outputs_value = outputs[['tx_id', 'value']].groupby('tx_id').sum()
merge_value_input = pd.merge(inputs_value, outputs_value, on ='tx_id')
invalid2 = merge_value_input.loc[merge_value_input['value_x'] != merge_value_input['value_y']]
print(invalid2)

# Invalid 3: The transaction's value of outut_id is unequal to its value of utxo.
outputs_sum = merge.groupby('output_id').sum()
# print(outputs_sum)
merge_value_output_id = pd.merge(outputs_sum,outputs[['output_id','value']], on ='output_id')
invalid3 = merge_value_output_id.loc[merge_value_output_id['value_x'] != merge_value_output_id['value_y']]
print(invalid3)




print("")
print("==================================End of Answer=================================================")

# Question B
inputs = pd.read_csv('inputs.csv')
outputs = pd.read_csv('outputs.csv')
tags = pd.read_csv('tags.csv')
transactions = pd.read_csv('transactions.csv')


# first cluster: according to the key, find the transaction
def cluster(inputs, key):
    pk = inputs.loc[inputs['sig_id']== key]
    if pk.empty:
        return []
    else:
        inputs_address = inputs.loc[inputs['tx_id'].isin(pk['tx_id'])]
        cluster_set = set(inputs_address['sig_id'])
    return cluster_set

# second cluster: according to the first cluster set find the remaining sig_id
def second_cluster(cluster_set):
    pk_remain = inputs.loc[inputs['sig_id'].isin(cluster_set)]
    tx_remain = inputs.loc[inputs['tx_id'].isin(pk_remain['tx_id'])]
    pk_remain_set = set(tx_remain.sig_id.unique())
    diff = pk_remain_set.difference(cluster_set)
    diff = list(diff)
    while (len(diff)> 0 ):
        cluster_set = cluster_set.union(pk_remain_set)
        pk_remain = inputs.loc[inputs['sig_id'].isin(cluster_set)]
        tx_remain = inputs.loc[inputs['tx_id'].isin(pk_remain['tx_id'])]
        pk_remain_set = set(tx_remain.sig_id.unique())
        diff = list(pk_remain_set.difference(cluster_set))

    print("Cluster is: ", pk_remain_set)
    print("Cluster size is: ", len(pk_remain_set))
    print("Max pk value is: ", max(pk_remain_set))
    print("Min pk value is: ", min(pk_remain_set))
    return pk_remain_set

# unspent: calculate the value of unspent bitcoins
def unspent(outputs, cluster_list):
    if (len(cluster_list) == 0):
        return -1
    else:
        unspent_coins = outputs.loc[outputs['pk_id'].isin(cluster_list)]

    print("Unspent bitcoin value: ", unspent_coins['value'].sum())
    return unspent_coins['value'].sum()

# Question a
second_cluster(cluster(inputs, 173091))
print("")
print("==================================End of Answer=================================================")

# Question b
inputs_txsig = pd.read_csv('inputs.csv', usecols=['tx_id', 'sig_id'])
# remove the duplicated sig_id
unique_sig = inputs_txsig['sig_id'].drop_duplicates(keep='first').dropna()
total_list = []

# use iteration to find the cluster contains maximum number of keys
for l in unique_sig:
    max_length = []
    c = second_cluster(cluster(inputs, l))
    max_length.append(c)

    if len(second_cluster(cluster(inputs,l))) == 921:
        cluster_mostkeys = second_cluster(cluster(inputs,l))

print(max(max_length))
# the result is 921
print ("The cluster contains most keys is:", cluster_mostkeys)
print("The number of keys is: ", len(cluster_mostkeys))
print("Max pk value is: ", max(cluster_mostkeys))
print("Min pk value is: ", min(cluster_mostkeys))
print("")
print("==================================End of Answer=================================================")

# Question c and Question d
used_coins = outputs.loc[outputs['id'].isin(inputs['output_id'])]
utxo = pd.concat([outputs, used_coins]).drop_duplicates(keep=False)
# find the valid utxo cluster
utxo_valid = utxo.loc[utxo['pk_id'].isin(inputs['sig_id'])]
# find the max value, use two empty lists
pk_id_list = []
for o in utxo_valid.pk_id.values:
    pk_id_list.append(o)

utxo_unspent_list= []
for p in pk_id_list:
    utxo_cluster = second_cluster(cluster(inputs, p))
    utxo_unspentvalue = unspent(utxo, utxo_cluster)
    utxo_unspent_list.append(utxo_unspentvalue)
    if utxo_unspentvalue == 4755624000000:
        utxo_pk = p

print("The answer of question c maximum unspent value is: ", max(utxo_unspent_list))
print("Bitcoin number is: ", max(utxo_unspent_list) * 0.00000001)
print("pk id is: ", utxo_pk)

second_cluster(cluster(inputs, utxo_pk))
tx = utxo.loc[utxo['pk_id'] == utxo_pk]
print(tx)
print("")
print("==================================End of Answer=================================================")

# Question f
bol = tags.loc[tags.name == 'Boloniex']
bollist = []
for i in bol.pk_id:
    bollist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
bol = sum(bollist)

pea = tags.loc[tags.name == 'PeakNevis']
pealist = []
for i in pea.pk_id:
    pealist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
pea = sum(pealist)

cat = tags.loc[tags.name == 'CatChange']
catlist = []
for i in cat.pk_id:
    catlist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
cat = sum(catlist)

gra = tags.loc[tags.name == 'Grafen']
gralist = []
for i in gra.pk_id:
    gralist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
gra = sum(gralist)

str = tags.loc[tags.name == 'StringRoad']
strlist = []
for i in str.pk_id:
    strlist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
str = sum(strlist)

bet = tags.loc[tags.name == 'BetaBay']
betlist = []
for i in bet.pk_id:
    betlist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
bet = sum(betlist)

lum = tags.loc[tags.name == 'LuminosX']
lumlist = []
for i in lum.pk_id:
    lumlist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
lum = sum(lumlist)

pen = tags.loc[tags.name == 'PennyBay']
penlist = []
for i in pen.pk_id:
    penlist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
pen = sum(penlist)

wem = tags.loc[tags.name == 'WembleyMarket']
wemlist = []
for i in wem.pk_id:
    wemlist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
wem = sum(wemlist)

swi = tags.loc[tags.name == 'SwindleWallet']
swilist = []
for i in swi.pk_id:
    swilist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
swi = sum(swilist)

hod = tags.loc[tags.name == 'HodlBase']
hodlist = []
for i in hod.pk_id:
    hodlist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
hod = sum(hodlist)


poc = tags.loc[tags.name == 'PocketFlex']
poclist = []
for i in poc.pk_id:
    poclist.append(unspent(utxo,second_cluster(cluster(inputs,i))))
poc = sum(poclist)

print(max(bol,pea,cat,gra,str,bet,lum,pen,wem,swi,hod,poc))
print("The unspent bitcoin value is: ", pea)
print("The unspent bitcoin number is: ", pea * 0.00000001)
print("")
print("==================================End of Answer=================================================")

# Question g
exchange = tags.loc[tags['type'] == 'Exchange']
dark = tags.loc[tags['type'] == 'DarkMarket']
input_list = []
output_list = []
for i in exchange.pk_id:
    a = second_cluster(cluster(inputs,i))
for j in dark.pk_id:
    b = second_cluster(cluster(inputs,j))
for i in a:
    input_list.append(i)
for i in b:
    output_list.append(i)

exchange_output = inputs.loc[inputs.sig_id.isin(input_list)]
dark_input = outputs.loc[outputs.pk_id.isin(output_list)]
tx_id = set(exchange_output.tx_id).intersection(set(dark_input.tx_id))
print(tx_id)
dark_tx_list = []
for i in tx_id:
    dark_tx_list.append(i)
dark_tx = outputs.loc[outputs.tx_id.isin(dark_tx_list)]
tx_value = sum(dark_tx['value'])
print("Bitcoin value: ", tx_value)
print("Bitcoin number: ",tx_value * 0.00000001)