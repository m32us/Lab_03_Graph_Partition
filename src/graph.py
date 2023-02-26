from vertex import *
from tqdm import tqdm


class Graph:
    def __init__(self):
        """
        Module constructing Graph class.
        """
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        """
        Module adding a vertex to Graph.

        :param key: vertex `key`
        :return: `key` as Vertex class
        """
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

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

    def BFS(self, vertex_ith):
        """
        Module applying Breadth First Search Algorithm.

        :param vertex_ith: the vertex id in Graph
        :return: path computed by BFS
        """
        vertex = self.getVertex(vertex_ith)  # get the vertex `vertex_ith`.
        if not vertex:  # checking if not exist `vertex_ith` in Graph then raise error
            message = 'Invalid vertex id, could not found vertex id `' + str(vertex_ith) + '` in Graph'
            raise ValueError(get_log(message, log_type='ERROR'))
        n = self.numVertices  # get the number of vertices.
        visited = [False] * n  # bool array for marking visited or not.
        vertex_id = vertex.getId()  # get the vertex_id for easy management.
        queue = [vertex_id]  # initializing a queue to handling which vertex is remaining.
        visited[vertex_id] = True  # marking the `vertex_id` is visited due to the beginning vertex.
        path = []  # path to track the working state of BFS.
        while queue:
            cur_pos = queue[0]  # handling current vertex before removing out of queue.
            path.append(cur_pos)  # appending to path to track.
            queue.pop(0)  # remove it out of queue
            neighbor_cur_pos = [x.id for x in self.getVertex(cur_pos).getConnections()]  # get all neighbors id of
            # current vertex.
            for neighborId in neighbor_cur_pos:  # loop over the neighbor of current vertex.
                if not visited[neighborId]:  # if not visited then push that vertex into queue.
                    visited[neighborId] = True
                    queue.append(neighborId)
        return path


def save_path(path: list, file_name=None, mode='stdout'):
    """
    Module writing path to screen or to file.

    :param path: path of searching result from BFS or DFS or other with the same structure.
    :param file_name: name of file to save result with `mode='write_to_file'`.
    :param mode: mode to write result to file (`mode='write_to_file'`) or to screen `mode='stdout'`.
    :return: Notification if save to file or warning empty if not exist path.
    """
    result = ['Beginning at vertex id: ' + str(path[0])]
    if not path:
        message = 'path is empty'
        print(get_log(message, log_type='WARNING'))
        return
    for vertex_id in path:  # collecting path data from `path`
        line = str(vertex_id)
        result.append(line)
    if mode.lower() == 'stdout':  # redirecting result to stdout of system
        print(get_log('Viewing mode: ' + mode.upper()))
        for line in result:
            print(get_log(line))
    elif mode.lower() == 'write_to_file':  # write result to file
        if not file_name:
            message = get_log('name of file is empty!', log_type='ERROR')
            raise ValueError(message)
        print(get_log('Viewing mode: ' + mode.upper()))
        print(get_log('WRITING RESULT TO FILE: ' + file_name))
        write_data = [result[0]]+['\n--> ' + line for line in result[1:]+['END']]
        with open(file_name, 'w') as f:
            for idx, line in zip(tqdm(range(len(write_data)), desc="Saving progress"), write_data):
                f.write(line)
            f.close()
        print(get_log('FINISHED SAVING DATA'))

