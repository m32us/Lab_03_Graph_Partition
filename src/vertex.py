from support import *


class Vertex:
    def __init__(self, key, label=None):
        """
        Module for initializing Vertex class.

        :param key: identifying vertex id by key.
        """
        self.id = key  # assigning `id` attribute by the input `key`.
        # handling which vertex is connected with this vertex.
        self.connectedTo = {}

        # Properties for graph partitioning
        self.level = 0
        self.partition_label = label

        self.external_cost = 0
        self.internal_cost = 0

    def addNeighbor(self, nbr, weight=0):
        """
        Module adding neighbor for Vertex.
        :param nbr: Vertex neighbor having connection with this vertex.
        :param weight: the weight of edge between this vertex and vertex `nbr`.
        :return:
        """
        self.connectedTo[nbr] = weight

    def __str__(self):
        """
        Module for show the information of vertex.

        :return: vertex id and its neighbors.
        """
        if self.partition_label is not None:
            return str(self.id) + ' (PL: ' + str(self.partition_label) + ')' + " connectedTo: " + str(
                [x.id for x in self.connectedTo])
        else:
            return str(self.id) + ' (lv ' + str(self.level) + ')' + " connectedTo: " + str(
                [x.id for x in self.connectedTo])

    def getConnections(self):
        """
        Module getting all neighbors of this vertex.

        :return: dict_keys() which saving all neighbors of this vertex.
        """
        return self.connectedTo.keys()

    def getId(self):
        """
        Module getting the `id` of this vertex.

        :return: `id` of this vertex.
        """
        return self.id

    def getWeight(self, nbr):
        """
        Module getting weight of connection between this vertex and vertex `nbr`.

        :param nbr: vertex has connection with this vertex.
        :return: weight of edge.
        """
        try:
            return self.connectedTo[nbr]
        except:
            return 0
