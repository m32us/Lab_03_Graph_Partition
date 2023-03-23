from support import get_log
import numpy as np

# Partitioning Algorithms

# Breadth First Search (BFS)


def pa_bfs(graph, vertex_ith: int, threshold: int):
    """Algorithm description:
        We can use basic graph search algorithm to solve graph partition algorithm :)
        Basically, the well-known BFS (Breadth-First-Search) algorithm can be modified to help us divide graph into two parts.
        BFS algorithm traverses the graph level by level and marks each vertex with the level in which it was visited. 
        After completion of the traversal, the set of vertices of the graph is portioned into two parts $V_1$ and $V_2$ by putting 
        all vertices with level less than or equal to a pre-determined threshold $L$ in the set V1 and putting the remaining vertices 
        (with level greater than $L$) in the set $V_2$. $L$ is so chosen that $|V1|$ is close to $|V2|$.

    References: 
    [1] Graph Partitioning, https://patterns.eecs.berkeley.edu/?page_id=571#1_BFS
    """
    L1 = set()
    L2 = set()

    # get the vertex `vertex_ith`.
    vertex = graph.getVertex(vertex_ith)

    # checking if not exist `vertex_ith` in Graph then raise error.
    if not vertex:
        message = 'Invalid vertex id, could not found vertex id `' + \
            str(vertex_ith) + '` in Graph'
        raise ValueError(get_log(message, log_type='ERROR'))

    # get the number of vertices.
    n = graph.numVertices

    # bool array for marking visited or not.
    visited = [False] * n

    # get the vertex_id for easy management.
    vertex_id = vertex.getId()

    # initializing a queue to handling which vertex is remaining.
    queue = [vertex_id]

    # marking the `vertex_id` is visited due to the beginning vertex.
    visited[vertex_id] = True

    path = []  # path to track the working state of BFS.

    level = 0
    while queue:
        # handling current vertex before removing out of queue.
        cur_pos = queue[0]

        # appending to path to track.
        path.append(cur_pos)

        # remove it out of queue
        queue.pop(0)

        # get all neighbors id of current vertex.
        neighbor_cur_pos = [
            x.id for x in graph.getVertex(cur_pos).getConnections()]

        # loop over the neighbor of current vertex.
        for neighborId in neighbor_cur_pos:
            # if not visited then push that vertex into queue.
            if not visited[neighborId]:
                visited[neighborId] = True
                graph.vertList[neighborId].level = level
                if level >= threshold:
                    L2.add(neighborId)
                else:
                    L1.add(neighborId)
                queue.append(neighborId)
        level += 1
    return L1, L2


# Kerninghan-Lin (KL) algorithm
def pa_kl(graph):
    """Algorithm description:
    The KL algorithm is a heuristic algorithm for partitioning a graph into two disjoint sets of vertices with roughly equal sizes, 
    while minimizing the total weight of the edges between the two sets. The algorithm works by iteratively swapping vertices 
    between the two sets in a way that reduces the total weight of the cut.

    The algorithm starts by dividing the vertices into two sets, A and B, with roughly equal sizes. 
    Then, it iteratively performs the following steps:
        Step 1: Compute the net gain for moving each vertex from set A to set B, and vice versa. 
        The net gain is defined as the difference between the sum of the weights of the edges 
        that connect the vertex to its current set and the sum of the weights of the edges 
        that connect the vertex to the other set.

        Step 2: Select the pair of vertices with the highest net gain, one from set A and one from set B, and swap them.

        Step 3: Update the net gains for the affected vertices, and repeat the process until no more swaps can be made.

    The algorithm terminates when no more swaps can be made that improve the total weight of the cut. 
    The final partitioning is the one that results in the minimum cut.

    References: 
    [1] Graph Partitioning, https://patterns.eecs.berkeley.edu/?page_id=571#1_BFS
    """
    # Partition the vertices into two equal-sized groups A and B.
    half = graph.numVertices // 2
    for ind in range(half):
        graph.vertList[ind].partition_label = 'A'
        graph.vertList[ind + half].partition_label = 'B'

    total_gain = 0

    # Keep track of the total gain in each iteration.
    for _ in range(half):
        # Get the vertices in groups A and B and their D values.
        group_a = [v.id for k, v in graph.vertList.items()
                   if v.partition_label == "A"]
        group_b = [v.id for k, v in graph.vertList.items()
                   if v.partition_label == "B"]

        D_values = {}

        for idx, vertex in graph.vertList.items():
            for neighbor in vertex.connectedTo:
                if vertex.partition_label == neighbor.partition_label:
                    vertex.internal_cost += vertex.getWeight(neighbor)
                else:
                    vertex.external_cost -= vertex.getWeight(neighbor)

            D_values.update(
                {idx: graph.vertList[idx].external_cost + graph.vertList[idx].internal_cost})

        # Compute the gains for all possible vertex swaps between groups A and B.
        gains = []
        for a in group_a:
            for b in group_b:
                c_ab = graph.vertList[a].getWeight(graph.vertList[b])
                gain = D_values[a] + D_values[b] - (2 * c_ab)
                gains.append([[a, b], gain])

        # Sort the gains in descending order and get the maximum gain.
        gains = sorted(gains, key=lambda x: x[1], reverse=True)
        max_gain = gains[0][1]

        if max_gain <= 0:
            break

        # Get the pair of vertices with the maximum gain and swap their partition labels.
        pair = gains[0][0]
        group_a.remove(pair[0])
        group_b.remove(pair[1])

        graph.vertList[pair[0]].partition_label = "B"
        graph.vertList[pair[1]].partition_label = "A"

        # Update the D values of the vertices in groups A and B.
        for x in group_a:
            c_xa = graph.vertList[x].getWeight(graph.vertList[pair[0]])
            c_xb = graph.vertList[x].getWeight(graph.vertList[pair[1]])
            D_values[x] += 2 * c_xa - 2 * c_xb

        for y in group_b:
            c_ya = graph.vertList[y].getWeight(graph.vertList[pair[0]])
            c_yb = graph.vertList[y].getWeight(graph.vertList[pair[1]])
            D_values[x] += 2 * c_ya - 2 * c_yb

        # Update the total gain.
        total_gain += max_gain

        # break

    # Get the cutset size and the vertex IDs in groups A and B.
    cutset_size = graph.compute_partition_cost()
    group_a = [v.id for k, v in graph.vertList.items()
               if v.partition_label == "A"]
    group_b = [v.id for k, v in graph.vertList.items()
               if v.partition_label == "B"]

    # Print the results
    print("Cut size: {}".format(cutset_size))
    print("Group A vertices: {}".format(group_a))
    print("Group B vertices: {}".format(group_b))

    return cutset_size, group_a, group_b


"""
The KL algorithm is a fast and effective heuristic for graph partitioning, and is widely used in practice. 
However, it is not guaranteed to find the optimal partitioning, and can get stuck in local minima. 
As a result, it is often used in combination with other algorithms or as a preprocessing step 
for more sophisticated partitioning algorithms.
"""

#########################################################################################################
# Fiduccia-Mattheyses (FM) algorithm


def pa_fm(graph):
    """Algorithm description:
    The FM algorithm is another popular heuristic algorithm for partitioning a graph into two disjoint sets of 
    vertices with roughly equal sizes, while minimizing the total weight of the edges between the two sets. 
    The algorithm works by iteratively moving vertices between the two sets in a way that reduces the total weight of the cut.

    The algorithm starts by dividing the vertices into two sets, A and B, with roughly equal sizes. 
    Then, it iteratively performs the following steps:
        Step 1: Compute the net gain for moving each vertex from set A to set B, and vice versa. 
        The net gain is defined as the difference between the sum of the weights of the edges 
        that connect the vertex to its current set and the sum of the weights of the edges 
        that connect the vertex to the other set.

        Step 2:  select one node according to some criterion, remove it from its present partition and put it to the other partition

        Step 3: Update the gains of the affected vertices, and repeat the process until no more vertices can be moved that 
        result in a decrease in the total weight of the cut.

    The algorithm terminates when no more vertices can be moved that result in a decrease in the total weight of the cut. 
    The final partitioning is the one that results in the minimum cut.

    References: 
    [1] Graph Partitioning, https://patterns.eecs.berkeley.edu/?page_id=571#1_BFS
    """

    # Partition the vertices into two equal-sized groups A and B.
    half = graph.numVertices // 2
    for ind in range(half):
        graph.vertList[ind].partition_label = 'A'
        graph.vertList[ind + half].partition_label = 'B'

    total_gain = 0

    # Keep track of the total gain in each iteration.
    for _ in range(half):
        # Get the vertices in groups A and B and their D values.
        group_a = [v.id for k, v in graph.vertList.items()
                   if v.partition_label == "A"]
        group_b = [v.id for k, v in graph.vertList.items()
                   if v.partition_label == "B"]

        D_values = {}

        for idx, vertex in graph.vertList.items():
            for neighbor in vertex.connectedTo:
                if vertex.partition_label == neighbor.partition_label:
                    vertex.internal_cost += vertex.getWeight(neighbor)
                else:
                    vertex.external_cost -= vertex.getWeight(neighbor)

            D_values.update(
                {idx: graph.vertList[idx].external_cost + graph.vertList[idx].internal_cost})

        # Compute the gains for all possible vertex swaps between groups A and B.
        gains = []
        for a in group_a:
            for b in group_b:
                c_ab = graph.vertList[a].getWeight(graph.vertList[b])
                gain = D_values[a] + D_values[b] - (2 * c_ab)
                gains.append([[a, b], gain])

        # Sort the gains in descending order and get the maximum gain.
        gains = sorted(gains, key=lambda x: x[1], reverse=True)
        min_gain = gains[-1][1]

        if min_gain <= 0:
            break

        # Get the pair of vertices with the maximum gain and swap their partition labels.
        pair = gains[0][0]
        group_a.remove(pair[0])
        group_b.remove(pair[1])

        graph.vertList[pair[0]].partition_label = "B"
        graph.vertList[pair[1]].partition_label = "A"

        # Update the D values of the vertices in groups A and B.
        for x in group_a:
            c_xa = graph.vertList[x].getWeight(graph.vertList[pair[0]])
            c_xb = graph.vertList[x].getWeight(graph.vertList[pair[1]])
            D_values[x] += 2 * c_xa - 2 * c_xb

        for y in group_b:
            c_ya = graph.vertList[y].getWeight(graph.vertList[pair[0]])
            c_yb = graph.vertList[y].getWeight(graph.vertList[pair[1]])
            D_values[x] += 2 * c_ya - 2 * c_yb

        # Update the total gain.
        total_gain += min_gain

        # break

    # Get the cutset size and the vertex IDs in groups A and B.
    cutset_size = graph.compute_partition_cost()
    group_a = [v.id for k, v in graph.vertList.items()
               if v.partition_label == "A"]
    group_b = [v.id for k, v in graph.vertList.items()
               if v.partition_label == "B"]

    # Print the results
    print("Cut size: {}".format(cutset_size))
    print("Group A vertices: {}".format(group_a))
    print("Group B vertices: {}".format(group_b))

    return cutset_size, group_a, group_b


"""
The FM algorithm is a fast and effective heuristic for graph partitioning, and is often used in combination with other algorithms 
or as a preprocessing step for more sophisticated partitioning algorithms. Like the KL algorithm, it is not guaranteed to find the 
optimal partitioning, and can get stuck in local minima. However, it is often faster and more scalable than the KL algorithm, making
it a popular choice for large-scale graph partitioning problems.
"""

#########################################################################################################
# Spectral Bisection


def pa_sb(graph):
    """Algorithm description:

    The Spectral Bisection algorithm is a graph partitioning algorithm that is based on the eigenvalues and eigenvectors of the graph Laplacian matrix. 
    The algorithm works by iteratively bisecting the graph into two disjoint sets of vertices with roughly equal sizes, while minimizing 
    the total weight of the edges between the two sets.

    The algorithm starts by computing the eigenvectors corresponding to the smallest eigenvalues of the graph Laplacian matrix. 
    The eigenvectors are then used to partition the graph into two sets of vertices, A and B, by assigning each vertex to 
    the set that corresponds to the sign of the corresponding eigenvector component. This initial partitioning is not guaranteed
    to be balanced, but is usually close to it.

    Then, the algorithm iteratively improves the partitioning by performing the following steps:
        Step 1: Compute the cut size of the current partitioning.
        Step 2: Compute the eigenvectors corresponding to the second-smallest eigenvalues of the graph Laplacian matrix.
        Step 3: Compute the projection of the current partitioning onto the space spanned by the eigenvectors corresponding 
        to the smallest and second-smallest eigenvalues. This projection is used to determine a new partitioning by assigning
        each vertex to the set that corresponds to the sign of the projection.
        Step 4: Compute the cut size of the new partitioning, and select it if it has a smaller cut size than the current partitioning. 
        Otherwise, discard the new partitioning and continue with the current one.

    The algorithm terminates when no more improvements can be made, or when a desired balance ratio between the two sets is achieved. 
    The final partitioning is the one that results in the minimum cut.

    References: 
    [1] Graph Partitioning, https://patterns.eecs.berkeley.edu/?page_id=571#1_BFS
    """
    laplacian_matrix = graph.compute_laplacian_matrix()
    print('Computing the eigenvectors and eigenvalues')
    eigenvalues, eigenvectors = np.linalg.eigh(laplacian_matrix)

    # Index of the second eigenvalue
    index_fnzev = np.argsort(eigenvalues)[1]
    print('Eigenvector for #{} eigenvalue ({}): '.format(
        index_fnzev, eigenvalues[index_fnzev]), eigenvectors[:, index_fnzev])

    # Partition on the sign of the eigenvector's coordinates
    partition = [val >= 0 for val in eigenvectors[:, index_fnzev]]

    # Compute the edges in between
    print(partition)
    a = [idx for (idx, group_label) in enumerate(partition) if group_label]
    b = [idx for (idx, group_label) in enumerate(partition) if not group_label]

    group_a = [v.id for k, v in graph.vertList.items()
               if v.id in a]
    group_b = [v.id for k, v in graph.vertList.items()
               if v.id in b]

    print("Group A vertices: {}".format(group_a))
    print("Group B vertices: {}".format(group_b))
    return group_a, group_b


"""
The Spectral Bisection algorithm is a powerful graph partitioning algorithm that can produce high-quality partitions for a wide range of graph types. 
However, it can be computationally expensive, especially for large graphs, due to the need to compute the eigenvalues and eigenvectors of the Laplacian matrix.
"""

#########################################################################################################
# k-way partitioning
# :)) lam bieng code qua