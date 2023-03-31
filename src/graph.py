import math

from vertex import *
from support import *

import numpy as np


class Graph:
    def __init__(self):
        """
        Module constructing Graph class.
        """
        self.vertList = {}
        self.numVertices = 0
        self.directedProp = True

    def addVertex(self, key, label=None):
        """
        Module adding a vertex to Graph.

        :param key: vertex `key`
        :return: `key` as Vertex class
        """
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key, label)
        self.vertList[key] = newVertex
        return newVertex

    def isDirected(self):
        return self.directedProp

    def getVertex(self, n):
        """
        Module returning Vertex `n` of Graph.

        :param n: the input vertex name `n`.
        :return: None if not exist else return Vertex `n`
        """
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        """
        Module to determine does vertex `n` belonged to Graph.

        :param n: vertex `n`.
        :return: True if belonged to Graph else False.
        """
        return n in self.vertList

    def addEdge(self, f, t, weight=0):
        """
        Module adding an Edge to Graph.

        :param f: the beginning vertex.
        :param t: the ending vertex.
        :param weight: the weight of that Edge.
        :return:
        """
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)
        if not self.isDirected():
            self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        """
        Module to get list vertex name of Graph.
        :return: list of vertex name.
        """
        return self.vertList.keys()

    def __iter__(self):
        """
        Module for looping with the vertices adjacency of each Vertex in Graph.
        :return: list adjacency of each vertex.
        """
        return iter(self.vertList.values())

    def BFS(self, vertex_ith: int):
        """
        Module applying Breadth First Search Algorithm.

        :param vertex_ith: the vertex id in Graph
        :return: path computed by BFS
        """
        vertex = self.getVertex(vertex_ith)  # get the vertex `vertex_ith`.
        if not vertex:  # checking if not exist `vertex_ith` in Graph then raise error
            message = 'Invalid vertex id, could not found vertex id `' + \
                      str(vertex_ith) + '` in Graph'
            raise ValueError(get_log(message, log_type='ERROR'))
        n = self.numVertices  # get the number of vertices.
        visited = [False] * n  # bool array for marking visited or not.
        vertex_id = vertex.getId()  # get the vertex_id for easy management.
        # initializing a queue to handling which vertex is remaining.
        queue = [vertex_id]
        # marking the `vertex_id` is visited due to the beginning vertex.
        visited[vertex_id] = True
        path = []  # path to track the working state of BFS.
        while queue:
            # handling current vertex before removing out of queue.
            cur_pos = queue[0]
            path.append(cur_pos)  # appending to path to track.
            queue.pop(0)  # remove it out of queue
            neighbor_cur_pos = [x.id for x in self.getVertex(
                cur_pos).getConnections()]  # get all neighbors id of
            # current vertex.
            for neighborId in neighbor_cur_pos:  # loop over the neighbor of current vertex.
                # if not visited then push that vertex into queue.
                if not visited[neighborId]:
                    visited[neighborId] = True
                    queue.append(neighborId)
        return path

    def DFS(self, vertex_ith: int):
        """depth first search function, start from `vertex_ith`

        Args:
            vertex_ith (int): key of vertex in graph

        Raises:
            ValueError: can't find a vertex with given key

        Returns:
            list[int]: the path that DFS agent has gone through
        """
        vertex: Vertex = self.getVertex(vertex_ith)
        if vertex is None:
            message = 'Invalid vertex id, could not found vertex id `' + \
                      str(vertex_ith) + '` in Graph'
            raise ValueError(get_log(message, log_type='ERROR'))

        closed_set: list[int] = []
        open_set: list[int] = [vertex.getId()]

        while open_set:
            cur_vertex: Vertex = self.getVertex(open_set.pop())
            cur_vertex_id = cur_vertex.getId()

            if cur_vertex_id not in closed_set:
                closed_set.append(cur_vertex_id)
                neighbors = [x.id for x in cur_vertex.getConnections()]

                for neighbor in neighbors:
                    if neighbor not in closed_set:
                        open_set.append(neighbor)
        return closed_set

    def reversing(self, ):
        rg = Graph()
        for i in range(self.numVertices):
            rg.addVertex(i)

        for vertex_idx, vertex in self.vertList.items():
            for neighbor in vertex.connectedTo:
                rg.addEdge(neighbor.getId(), vertex.getId(),
                           neighbor.getWeight(vertex))

        return rg

    def find_strongly_connected_components(self):
        """
        Kosaraju algorithm
        """
        # Perform a Depth First Search (DFS) on the original graph 
        # and keep track of the order in which the nodes are visited.
        dfspath = self.DFS()

        # Reverse the directions of all edges in the graph to obtain a new graph.
        rg = self.reversing()

        # Perform a DFS on the new graph, visiting the nodes in the reverse order obtained in step 1. 
        # As you perform the DFS, mark each node as belonging to the same SCC.
        closed_set: list[int] = []
        scc_set = []

        for idx in range(rg.numVertices):
            if idx not in closed_set:
                # open_set: list[int] = [idx]
                scc = []

                while dfspath:
                    cur_vertex: Vertex = rg.getVertex(dfspath.pop())
                    cur_vertex_id = cur_vertex.getId()

                    if cur_vertex_id not in closed_set:
                        closed_set.append(cur_vertex_id)
                        scc.append(cur_vertex_id)

                        neighbors = [x.id for x in cur_vertex.getConnections()]

                        for neighbor in neighbors:
                            if neighbor not in closed_set:
                                dfspath.append(neighbor)
                scc_set.append(scc)

        return scc_set

    def compute_partition_cost(self):
        """Computing partiion cost function
        Returns:
            int: partiion cost for each partition in graph.
        """

        cost = []
        for vertex_idx, vertex in self.vertList.items():
            for neighbor in vertex.connectedTo.keys():
                if vertex.partition_label != neighbor.partition_label:
                    cost.append(vertex.getWeight(neighbor))
        return sum(cost)

    def compute_adjacency_matrix(self, ):
        """Computing adjacency matrix for graph
        Returns:
            np.darray: adjacency matrix for graph
        """
        adjacency_matrix = np.zeros((self.numVertices, self.numVertices))
        for vertex_idx, vertex in self.vertList.items():
            for neighbor in vertex.connectedTo:
                adjacency_matrix[vertex_idx][neighbor.id] = vertex.getWeight(
                    neighbor)
        return adjacency_matrix

    def degree_nodes(self, adjacency_matrix):
        """Compute the degree of each node
        Returns:
            np.darray: the vector of degrees
        """
        d = []
        for idx in range(self.numVertices):
            d.append(sum([1 if adjacency_matrix[idx][jdx] !=
                               0 else 0 for jdx in range(self.numVertices)]))
        return d

    def compute_laplacian_matrix(self, ):
        """Compute the Laplacian matrix for graph.
        Returns:
            np.darray: the Laplacian matrix for graph.
        """
        # print('Computing Adjacency Matrix')
        adjacency_matrix = self.compute_adjacency_matrix()
        # print('Computing the degree of each node')
        degrees = self.degree_nodes(adjacency_matrix)
        # print('Computing the Laplacian matrix')
        laplacian_matrix = np.diag(degrees) - adjacency_matrix
        return laplacian_matrix

    def compute_total_weight(self):
        total = 0
        for vertex in self.vertList.values():
            for neighbor in vertex.getConnections():
                total += vertex.getWeight(neighbor)

        if self.isDirected():
            return total
        return total // 2

    def initialize_label(self):
        half = self.numVertices // 2
        for ind in range(half):
            self.vertList[ind].partition_label = 'A'
            self.vertList[ind + half].partition_label = 'B'

    def get_edge_weight_bfs(self, v1, v2):
        if v1 == v2:
            return 0
        vertex = self.getVertex(v1)  # get the vertex `vertex_ith`.
        if not vertex:  # checking if not exist `vertex_ith` in Graph then raise error
            message = 'Invalid vertex id, could not found vertex id `' + \
                      str(v1) + '` in Graph'
            raise ValueError(get_log(message, log_type='ERROR'))
        n = self.numVertices  # get the number of vertices.
        visited = [False] * n  # bool array for marking visited or not.
        vertex_id = vertex.getId()  # get the vertex_id for easy management.
        # initializing a queue to handling which vertex is remaining.
        queue = [(vertex_id, 0)]
        # marking the `vertex_id` is visited due to the beginning vertex.
        visited[vertex_id] = True
        while queue:
            # handling current vertex before removing out of queue.
            cur_pos, distance = queue[0]
            queue.pop(0)  # remove it out of queue
            vertex_cur = self.getVertex(cur_pos)
            # current vertex.
            for neighbor in vertex_cur.getConnections():  # loop over the neighbor of current vertex.
                neighborId = neighbor.getId()
                if v2 == neighborId:
                    return vertex_cur.getWeight(neighbor)
                # if not visited then push that vertex into queue.
                if not visited[neighborId]:
                    visited[neighborId] = True
                    queue.append((neighborId, distance + vertex_cur.getWeight(neighbor)))
        return math.inf
