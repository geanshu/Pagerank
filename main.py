from dataload import Graph
import heapq
import math


class Pagerank:
    def __init__(self, max_iter=100, alpha=0.85):
        self.alpha = alpha
        self.max_iter = max_iter

        graph = Graph()
        self.N = graph.N
        self.nodes = graph.nodes
        self.PR = [1.0 / self.N] * self.N
        self.dead_nodes = []
        self.out_degree = dict()
        for i in range(self.N):
            out_d = graph.out_degree[self.nodes[i]]
            for j in range(len(out_d)):
                out_d[j] = self.nodes.index(out_d[j])
            self.out_degree[i] = (len(out_d), out_d)
            if len(out_d) == 0:
                self.dead_nodes.append(i)

    def block_process(self, block_size):
        block_list = []
        for i in range(math.ceil(self.N / block_size)):
            start, end = i * block_size, min(self.N, (i + 1) * block_size)
            block = dict()
            for src, (d, out_d) in self.out_degree.items():
                block_d = list(filter(lambda x: start <= x < end, out_d))
                if len(block_d) > 0:
                    block[src] = (d, block_d)
            block_list.append(block)
        return block_list

    def block_cal_PR(self, block_size=1000):
        if block_size < self.N:
            block_list = self.block_process(block_size)
        else:
            block_list = [self.out_degree]
        for i in range(self.max_iter):
            new_PR = []
            loss = 0
            for block_id, block in enumerate(block_list):
                start, end = block_id * block_size, min(self.N, (block_id + 1) * block_size)
                block_PR, block_loss = self.block_iter(self.PR, block, self.dead_nodes, start, end, self.alpha)
                new_PR += block_PR
                loss += block_loss
            self.PR = new_PR
            print("iter %2d: %f" % (i, loss))
            if loss <= 1e-6 * self.N:
                break
        self.out_res()
        return self.PR

    def block_iter(self, PR, out_degree, dead_nodes, start, end, alpha=0.85):
        loss = 0
        N = len(PR)
        dead_node_sum = alpha * sum(PR[n] for n in dead_nodes) / N
        new_PR = [(1 - alpha) / N + dead_node_sum] * (end-start)
        for src, (d, out_d) in out_degree.items():
            for out_node in out_d:
                new_PR[out_node-start] += alpha*PR[src]/d
        for i in range(end-start):
            loss += abs(new_PR[i]-PR[start+i])
        return new_PR, loss

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
    p.block_cal_PR(int(input("block-size: ")))

