import pandas as pd

# # Question b

# # print(tx_id_stat)
# # according to 'value_counts', the first element contains largest number of keys
# inputs_clustermax = inputs.loc[inputs['tx_id'] == tx_id_stat.index[0]]
# # remove the duplicated sig_id
# inputs_clustermax = inputs_clustermax['sig_id'].drop_duplicates(keep='first')
# print("Biggest cluster is: ", inputs_clustermax)
# print("Biggest cluster size: ",len(inputs_clustermax))
# print("Largest value: ",max(inputs_clustermax))
# print("Lowest value: ",min(inputs_clustermax))
# print("")
# print("==================================End of Answer=================================================")





# Question g
# exchange = tags.loc[tags['type'] == 'Exchange']
# darketmarket = tags.loc[tags['type'] == 'DarkMarket']
# exchange_list = []
# darketmarket_list = []
#
# for r in exchange['pk_id']:
#     exchange_list = np.append(exchange_list,cluster(inputs, r))
# # print(exchange_list)
#
# for s in darketmarket['pk_id']:
#     darketmarket_list.append(s)
# # print(darketmarket_list)
#
# darketmarket_input = outputs.loc[outputs['pk_id'].isin(darketmarket_list)]
# # print(darketmarket_input)
#
# darketmarket_input_list = []
# for t in darketmarket_input['tx_id']:
#     darketmarket_input_list.append(t)
#
# exchange_input = inputs.loc[inputs['sig_id'].isin(exchange_list)]
# exchange_output = exchange_input.loc[exchange_input['tx_id'].isin(darketmarket_input_list)]
# exchange_output_tx_id = exchange_output['tx_id'].unique()
# print("Transaction: ",exchange_output_tx_id," sent bitcoins directly from a (fictional) exchange to a (fictional) dark market.")
# # [ 57450  57746  59456  59618  86621 104152 111248]
#
# sum_value = 0
# for u in exchange_output_tx_id:
#         sum_value = sum_value + darketmarket_input.loc[darketmarket_input['tx_id'] == u]['value'].values
# sum_value = list(sum_value).pop()
# print("The total value is: ", sum_value, " satoshis.")
# print("The number of bitcoins is: ", sum_value*0.00000001)
# print("")
# print("==================================End of Answer=================================================")
