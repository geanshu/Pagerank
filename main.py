from dataload import Graph
import numpy as np
import heapq
import math


class Pagerank:
    def __init__(self, max_iter=100, block_size=1000, alpha=0.85):
        self.p = alpha
        self.max_iter = max_iter
        self.block_size = block_size

        self.graph = Graph()
        self.N = self.graph.N
        self.in_degree = self.graph.in_degree
        self.nodes = self.graph.nodes
        self.PR = np.ones(self.graph.N)
        self.PR_init()

    def PR_init(self):
        self.V = np.zeros(self.graph.N)  # 转移矩阵,每个节点出度数量
        for i in range(self.graph.N):
            node = self.graph.nodes[i]
            out = self.graph.out_degree[node]
            self.V[i] = len(out)
        self.in_degree = sorted(list(self.in_degree.items()), key=lambda e: e[0])
        for i in range(len(self.in_degree)):
            self.in_degree[i] = self.in_degree[i][1]
        del self.graph

    def PR_iter(self):
        for i in range(self.N):
            new_PR = (1 - self.p) / self.N
            for e in self.in_degree[i]:
                node = self.nodes.index(e)
                new_PR += self.p * self.PR[node] / self.V[node]
            self.PR[i] = new_PR
        return

    def cal_PR(self):
        for i in range(self.max_iter):
            self.PR_iter()
            print("iter %3d finish" % i)
        self.out_res()

    def block_cal_PR(self):
        for i in range(self.max_iter):
            block_PR = None
            for j in range(math.ceil(self.N / self.block_size)):
                start, end = j * self.block_size, min(self.N, (j + 1) * self.block_size)
                g = np.zeros((end - start, self.N), dtype=np.float64)
                for num in range(start, end):
                    for node in self.in_degree[num]:
                        idx_node = self.nodes.index(node)
                        g[num - start, idx_node] = 1 / self.V[idx_node]
                if block_PR is not None:
                    block_PR = np.concatenate([block_PR, self.block_process(self.PR, g, self.p)], axis=0)
                else:
                    block_PR = self.block_process(self.PR, g, self.p)
            self.PR = block_PR
            print("iter %3d finish" % i)
        self.out_res()

    def out_res(self):
        res = heapq.nlargest(100, enumerate(self.PR), key=lambda x: x[1])
        top_id = []
        for i, (idx, pr) in enumerate(res):
            print("Top %3d: %4d %6f" % (i, self.nodes[idx], pr))
            top_id.append((self.nodes[idx], pr))
        with open('result.txt', 'w') as f:
            for item in top_id:
                f.write("%d %f\n" % (item[0], item[1]))

    @staticmethod
    def block_process(PR, graph, p):
        res = p * np.dot(graph, PR)
        return np.ones(res.size) * (1 - p) / PR.size + res


if __name__ == '__main__':
    p = Pagerank()
    p.block_cal_PR()
    # p.cal_PR()
