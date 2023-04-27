from dataload import Graph
from heapq import nlargest
from math import ceil
from os import system, remove


class Block:
    def __init__(self, out_degree, block_size, N):
        self.N = N
        if block_size < N:
            block_list = self.block_process(out_degree, block_size)
        else:
            block_list = [out_degree]
        self.block_num = self.save_block(block_list)

    def block_process(self, out_degree, block_size):
        block_list = []
        for i in range(ceil(self.N / block_size)):
            start, end = i * block_size, min(self.N, (i + 1) * block_size)
            block = dict()
            for src, (d, out_d) in out_degree.items():
                block_d = list(filter(lambda x: start <= x < end, out_d))
                if len(block_d) > 0:
                    block[src] = (d, block_d)
            block_list.append(block)
        return block_list

    def save_block(self, block_list):
        for idx, block in enumerate(block_list):
            with open('block_%d.txt' % idx, 'w') as f:
                for src, (d, out_d) in block.items():
                    data = "%d,%d," % (src, d) + str(out_d)[1:-1] + '\n'
                    f.write(data)
        return len(block_list)

    def read_block(self, id):
        block = dict()
        with open('block_%d.txt' % id, 'r') as f:
            for line in f:
                data = line.strip('\n').split(',')
                if data[1] == '0':
                    data = data[:2]
                data = list(map(int, data))
                block[data[0]] = (data[1], data[2:])
        return block

    def __del__(self):
        for i in range(self.block_num):
            remove('block_%d.txt' % i)


class PR:
    def __init__(self, N):
        self.data = [1.0 / N] * N

    def save_PR(self, PR_block, id):
        if id == 0:
            f = open('PR.txt', 'w')
        else:
            f = open('PR.txt', 'a')
        f.write(str(PR_block)[1:-1].replace(',', '\n') + '\n')

    def load_PR(self):
        self.data = []
        with open('PR.txt', 'r') as f:
            self.data = str(f.read()).split('\n')[:-1]
        self.data = list(map(float, self.data))
        remove('PR.txt')


class Pagerank:
    def __init__(self, data='Data.txt', max_iter=100, alpha=0.85):
        self.alpha = alpha
        self.max_iter = max_iter
        graph = Graph(data)
        self.N = graph.N
        self.nodes = graph.nodes
        self.PR = PR(self.N)
        self.dead_nodes = []
        self.out_degree = dict()
        for i in range(self.N):
            out_d = graph.out_degree[self.nodes[i]]
            for j in range(len(out_d)):
                out_d[j] = self.nodes.index(out_d[j])
            self.out_degree[i] = (len(out_d), out_d)
            if len(out_d) == 0:
                self.dead_nodes.append(i)

    def block_cal_PR(self, block_size=1000):
        block_list = Block(self.out_degree, block_size, self.N)
        del self.out_degree
        for i in range(self.max_iter):
            loss = 0
            for block_id in range(block_list.block_num):
                start, end = block_id * block_size, min(self.N, (block_id + 1) * block_size)
                block_PR, block_loss = self.block_iter(self.PR.data, block_list.read_block(block_id), self.dead_nodes,
                                                       start, end, self.alpha)
                self.PR.save_PR(block_PR, block_id)
                loss += block_loss
            self.PR.load_PR()
            print("iter %2d: %f" % (i, loss))
            if loss <= 1e-6 * self.N:
                break
        self.out_res()
        return

    def block_iter(self, PR, out_degree, dead_nodes, start, end, alpha=0.85):
        loss = 0
        N = len(PR)
        dead_node_sum = alpha * sum(PR[n] for n in dead_nodes) / N
        new_PR = [(1 - alpha) / N + dead_node_sum] * (end - start)
        for src, (d, out_d) in out_degree.items():
            for out_node in out_d:
                new_PR[out_node - start] += alpha * PR[src] / d
        for i in range(end - start):
            loss += abs(new_PR[i] - PR[start + i])
        return new_PR, loss

    def out_res(self):
        res = nlargest(100, enumerate(self.PR.data), key=lambda x: x[1])
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
    system("pause")
