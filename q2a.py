# Get a list of public keys sets that used as input to the same transaction
tx_input_counts = inputs_df.tx_id.value_counts()
tx_with_more_than_one_input = tx_input_counts[tx_input_counts>1]
pub_keys_in_tx_with_multi_inputs = []
for tx in tx_with_more_than_one_input.index:
    inputs = inputs_df[inputs_df.tx_id == tx]
    if len(set(inputs.sig_id.values))>1:
        pub_keys_in_tx_with_multi_inputs.append(set(inputs.sig_id.values))

# See if these key sets can be merged
# The function iterate through a list of key sets once and check whether the cluster can merge with these sets
def iterate_once_and_merge(cluster, other_clusters):
    updated = False
    remaining_clusters = list(other_clusters)
    for other_cluster in other_clusters:
        if cluster.intersection(other_cluster):
            cluster = cluster.union(other_cluster)
            remaining_clusters.remove(other_cluster)
            updated = True
    return updated, cluster, remaining_clusters

# Iterate through every sets until they are all merged where possible
clusters = []
while len(pub_keys_in_tx_with_multi_inputs)>1:
    cluster = pub_keys_in_tx_with_multi_inputs[0]
    other_clusters = pub_keys_in_tx_with_multi_inputs[1:]
    updated = True
    while updated:
        updated, cluster, other_clusters = iterate_once_and_merge(cluster, other_clusters)
    clusters.append(cluster)
    pub_keys_in_tx_with_multi_inputs = other_clusters
if len(pub_keys_in_tx_with_multi_inputs) == 1:
    clusters.append(pub_keys_in_tx_with_multi_inputs[0])
# Finally obtain the clusters based on multi-input heuristic
print(clusterfun(inputs,41442))
print(clusterfun(inputs,138871))
