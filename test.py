import networkx as nx

if __name__ == '__main__':
    edges = []
    with open('Data.txt', 'r') as f:
        for data in f.readlines():
            data = data.strip('\n').split(' ')
            edges.append((int(data[0]), int(data[1])))
    edges = list(set(edges))

    G = nx.DiGraph()
    G.add_edges_from(edges)
    pagerank_list = nx.pagerank(G, alpha=0.85, max_iter=100)

    res = sorted(pagerank_list.items(), key=lambda e: e[1], reverse=True)[:100]
    for d in res:
        print(d)
