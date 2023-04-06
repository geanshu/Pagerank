class Graph:
    def __init__(self, fname='Data.txt'):
        self.nodes, self.edges = self.load_data(fname)
        self.in_degree, self.out_degree = self.construct_map(self.nodes, self.edges)
        self.N = len(self.nodes)
        self.E = len(self.edges)

    @staticmethod
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

    @staticmethod
    def construct_map(nodes, edges):
        out_degree_map = {}
        in_degree_map = {}
        for n1, n2 in edges:
            if n1 in out_degree_map:
                out_degree_map[n1].append(n2)
            else:
                out_degree_map[n1] = [n2]
            if n2 in in_degree_map:
                in_degree_map[n2].append(n1)
            else:
                in_degree_map[n2] = [n1]
        for node in nodes:
            if node not in out_degree_map:
                out_degree_map[node] = []
            if node not in in_degree_map:
                in_degree_map[node] = []
        return in_degree_map, out_degree_map
