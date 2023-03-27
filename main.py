from dataload import Graph
import numpy as np

class Pagerank:
    def __init__(self, iter_num):
        self.p = 0.85
        self.graph = Graph()
        self.PR = dict()
        self.iter_num = iter_num
    def init_PR(self):
        for node in self.graph.nodes:
            self.PR[node] = [0] * self.graph.N
            for in_node in self.graph.in_degree[node]:
                self.PR[node][self.graph.nodes.index(in_node)] = 1/len(self.graph.out_degree[in_node])
        return


if __name__ == '__main__':
    p = Pagerank()




