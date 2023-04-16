from dataload import Graph
import heapq
import math


class Pagerank:
    def __init__(self, max_iter=100, alpha=0.85):
        self.alpha = alpha
        self.max_iter = max_iter

        self.graph = Graph()
        self.N = self.graph.N
        self.nodes = self.graph.nodes
        self.PR = [1.0/self.N] * self.N
        self.PR_init()

    def PR_init(self):
        self.V = [0] * self.N  # 节点出度数量
        for i in range(self.graph.N):
            node = self.graph.nodes[i]
            self.V[i] = len(self.graph.out_degree[node])

        self.dead_nodes = []
        for idx, d in enumerate(self.V):
            if d == 0:
                self.dead_nodes.append(idx)

        self.in_degree = []
        for i in range(self.N):
            in_d = self.graph.in_degree[self.nodes[i]]
            for j in range(len(in_d)):
                in_d[j] = self.nodes.index(in_d[j])
            self.in_degree.append(in_d)
        del self.graph

    @staticmethod
    def PR_iter(V, in_degree, PR, dead_nodes, alpha=0.85):
        loss = 0
        N = len(PR)
        dead_node_sum = alpha * sum(PR[n] for n in dead_nodes) / N
        new_PR = [(1 - alpha) / N + dead_node_sum] * N
        for i in range(N):
            for e in in_degree[i]:
                node = e
                new_PR[i] += alpha * PR[node] / V[node]
            loss += abs(PR[i] - new_PR[i])
        return new_PR, loss

    def cal_PR(self):
        for i in range(self.max_iter):
            self.PR, loss = self.PR_iter(self.V, self.in_degree, self.PR, self.dead_nodes, self.alpha)
            print("iter %2d: %f" % (i, loss))
            if loss <= 1e-6 * self.N:
                break
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


if __name__ == '__main__':
    p = Pagerank()
    p.cal_PR()
    # p.stripe_block()
