from dataload import Graph
import numpy as np
import heapq

class Pagerank:
    def __init__(self, iter_num):
        self.p = 0.85
        self.graph = Graph()
        self.PR = np.ones(self.graph.N)
        self.iter_num = iter_num
        self.PR_init()

    def PR_init(self):
        self.V = np.zeros(self.graph.N)  # 转移矩阵
        for i in range(self.graph.N):
            node = self.graph.nodes[i]
            out = self.graph.out_degree[node]
            self.V[i] = len(out)
        del self.graph.out_degree
    def PR_iter(self):
        for i in range(self.graph.N):
            new_PR = (1-self.p) / self.graph.N
            for e in self.graph.in_degree[self.graph.nodes[i]]:
                node = self.graph.nodes.index(e)
                new_PR += self.p * self.PR[node]/self.V[node]
            self.PR[i] = new_PR
        return

    def cal_PR(self):
        for i in range(self.iter_num):
            self.PR_iter()
        res = heapq.nlargest(100, enumerate(self.PR), key=lambda x: x[1])
        top_id = []
        for idx, pr in res:
            top_id.append(self.graph.nodes[idx])
        print(top_id)


if __name__ == '__main__':
    p = Pagerank(100)
    p.cal_PR()




