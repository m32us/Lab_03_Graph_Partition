from graph import *

from algorithms import pa_bfs, pa_kl, pa_sb

# main
g = Graph()
for i in range(6):
    g.addVertex(i)
g.addEdge(0, 1, 5)
g.addEdge(0, 5, 2)
g.addEdge(1, 2, 4)
g.addEdge(2, 3, 9)
g.addEdge(3, 4, 7)
g.addEdge(3, 5, 3)
g.addEdge(4, 0, 1)
g.addEdge(5, 4, 8)
g.addEdge(5, 2, 1)


# lst_vertices = g.vertList

pa_sb(g)

# pa_kl(g)
# g.compute_adjacency_matrix()
# g.degree_nodes()

# for k, v in g.vertList.items():
#     print(v)
#     for key, item in v.connectedTo.items():
#         print(v.getWeight(key))

#     print('----')

# print(L1)
# print(L2)

# print(g.weight_func(1, 0))
