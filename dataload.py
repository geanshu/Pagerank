
def load_data(fname):
    node_list = []
    edge_pair_list = []
    with open(fname, 'r') as f:
        for data in f.readlines():
            data = data.strip('\n').split(' ')
            n1 = int(data[0])
            n2 = int(data[1])
            if n1 not in node_list:
                node_list.append(n1)
            if n2 not in node_list:
                node_list.append(n2)
            edge_pair_list.append((n1, n2))
    node_list = sorted(node_list)
    return node_list, edge_pair_list


def construct_map(nodes, edges):
    map_dict = {}
    for n1, n2 in edges:
        if n1 in map_dict:
            map_dict[n1].append(n2)
        else:
            map_dict[n1] = [n2]
    return map_dict

nodes, edges = load_data('Data.txt')
construct_map(nodes, edges)