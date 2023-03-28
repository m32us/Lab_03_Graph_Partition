# Lab 03: IMPLEMENT SOME GRAPH PARTITION ALGORITHMS.

Graph partitioning is the process of dividing a graph into multiple subgraphs or partitions, such that each subgraph is connected and has a certain desirable property, such as balanced size or minimal cut size. Although it is a challenging problem, finding a partition that makes graph analysis easier has applications in scientific computing. In this project, we provide a Python programming language implementation for a few well-known graph partitioning techniques.

## Problem statement

Considering a graph  $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where $\mathcal{V}$ denotes the set of $n$ vertices and $\mathcal{E}$ donates the set of edges.

For a $(k, v)$ balanced partition problem, the objective is to partition $\mathcal{G}$ into $k$ components of at most size $v \cdot \frac{n}{k}$ while minimizing the capacity of the edges between separate components[1].

## Graph partition methods

### Breadth First Search (BFS)

Basically, the well-known BFS (Breadth-First-Search) algorithm can be modified to help us divide graph into two parts.
BFS algorithm traverses the graph level by level and marks each vertex with the level in which it was visited. 
After completion of the traversal, the set of vertices of the graph is portioned into two parts $V_1$ and $V_2$ by putting 
all vertices with level less than or equal to a pre-determined threshold $L$ in the set V1 and putting the remaining vertices 
(with level greater than $L$) in the set $V_2$. $L$ is so chosen that $|V1|$ is close to $|V2|$.

### Kerninghan-Lin (KL) algorithm

The KL algorithm is a heuristic algorithm for partitioning a graph into two disjoint sets of vertices with roughly equal sizes, 
while minimizing the total weight of the edges between the two sets. The algorithm works by iteratively swapping vertices 
between the two sets in a way that reduces the total weight of the cut.

The algorithm starts by dividing the vertices into two sets, A and B, with roughly equal sizes. 
Then, it iteratively performs the following steps:
- Step 1: Compute the net gain for moving each vertex from set A to set B, and vice versa. The net gain is defined as the difference between the sum of the weights of the edges that connect the vertex to its current set and the sum of the weights of the edges that connect the vertex to the other set.
- Step 2: Select the pair of vertices with the highest net gain, one from set A and one from set B, and swap them.
- Step 3: Update the net gains for the affected vertices, and repeat the process until no more swaps can be made.

The algorithm terminates when no more swaps can be made that improve the total weight of the cut. The final partitioning is the one that results in the minimum cut.

The KL algorithm is a fast and effective heuristic for graph partitioning, and is widely used in practice. However, it is not guaranteed to find the optimal partitioning, and can get stuck in local minima. As a result, it is often used in combination with other algorithms or as a preprocessing step for more sophisticated partitioning algorithms.

### Fiduccia-Mattheyses (FM) algorithm

The FM algorithm is another popular heuristic algorithm for partitioning a graph into two disjoint sets of vertices with roughly equal sizes, while minimizing the total weight of the edges between the two sets. The algorithm works by iteratively moving vertices between the two sets in a way that reduces the total weight of the cut.

The algorithm starts by dividing the vertices into two sets, A and B, with roughly equal sizes. Then, it iteratively performs the following steps:
- Step 1: Compute the net gain for moving each vertex from set A to set B, and vice versa. The net gain is defined as the difference between the sum of the weights of the edges that connect the vertex to its current set and the sum of the weights of the edges that connect the vertex to the other set.
- Step 2: Select one node according to some criterion, remove it from its present partition and put it to the other partition
- Step 3: Update the gains of the affected vertices, and repeat the process until no more vertices can be moved that result in a decrease in the total weight of the cut.

The algorithm terminates when no more vertices can be moved that result in a decrease in the total weight of the cut. The final partitioning is the one that results in the minimum cut.

The FM algorithm is a fast and effective heuristic for graph partitioning, and is often used in combination with other algorithms or as a preprocessing step for more sophisticated partitioning algorithms. Like the KL algorithm, it is not guaranteed to find the  optimal partitioning, and can get stuck in local minima. However, it is often faster and more scalable than the KL algorithm, making it a popular choice for large-scale graph partitioning problems.

### Spectral Bisection

The Spectral Bisection algorithm is a graph partitioning algorithm that is based on the eigenvalues and eigenvectors of the graph Laplacian matrix. The algorithm works by iteratively bisecting the graph into two disjoint sets of vertices with roughly equal sizes, while minimizing the total weight of the edges between the two sets.

The algorithm starts by computing the eigenvectors corresponding to the smallest eigenvalues of the graph Laplacian matrix. The eigenvectors are then used to partition the graph into two sets of vertices, A and B, by assigning each vertex to the set that corresponds to the sign of the corresponding eigenvector component. This initial partitioning is not guaranteed to be balanced, but is usually close to it.

Then, the algorithm iteratively improves the partitioning by performing the following steps:
- Step 1: Compute the cut size of the current partitioning.
- Step 2: Compute the eigenvectors corresponding to the second-smallest eigenvalues of the graph Laplacian matrix.
- Step 3: Compute the projection of the current partitioning onto the space spanned by the eigenvectors corresponding to the smallest and second-smallest eigenvalues. This projection is used to determine a new partitioning by assigning each vertex to the set that corresponds to the sign of the projection.
- Step 4: Compute the cut size of the new partitioning, and select it if it has a smaller cut size than the current partitioning. Otherwise, discard the new partitioning and continue with the current one.

The algorithm terminates when no more improvements can be made, or when a desired balance ratio between the two sets is achieved. The final partitioning is the one that results in the minimum cut.

The Spectral Bisection algorithm is a powerful graph partitioning algorithm that can produce high-quality partitions for a wide range of graph types. 
However, it can be computationally expensive, especially for large graphs, due to the need to compute the eigenvalues and eigenvectors of the Laplacian matrix.

## Setup
We just install the *datetime* library only for logging status. If you don't have just reinstall by using the below command.

```
pip install datetime
```
## Structure of Library

1.  Vertex class
    
    - The **Vertex** class contains 2 features as below:
     
      - `id`: used to identify the the vertex in Graph.
     
      - `connectedTo`: handling which vertex is connected with this vertex.
      - Properties for graph partitioning: `level`, `partition_label`, `external_cost`, `internal_cost`
    
    - Functions:
     
        - `addNeighbor(self, nbr, weight=0)`: module adding neighbor for Vertex.

        - `__str__(self)`: module for show the information of vertex.

        - `getId(self)`: module getting the `id` of this vertex.

        - `getWeight(self, nbr)`: module getting weight of connection between this vertex and vertex `nbr`.

    
2.  Graph class

    - The **Graph** class is our main class for managing and contains main functions to organise and work with graph data. It has 2 main components including:
      
      - `vertList`: saving all vertices of Graph, each element is a Vertex identified by its `id`.
      
      - `numVertices`: is the number of vertices.

    - Functions:
        
        - `addVertex(self, key)`: module adding a vertex to Graph.
        
        - `getVertex(self, n)`: module returning Vertex `n` of Graph.
        
        - `__contains__(self, n)`: module to determine does vertex `n` belonged to Graph.
        
        - `addEdge(self, f, t, weight=0)`: module adding an Edge to Graph.

        -  `getVertices(self)`: module to get list vertex name of Graph.
        
        - `__iter__(self)`: module for looping with the vertices adjacency of each Vertex in Graph.

        - `BFS(self, vertex_ith: int)`: module applying Breadth First Search Algorithm.
        
        - `DFS(self, vertex_ith: int)`: module applying Depth First Search Algorithm.
        - `compute_adjacency_matrix(self, )`: computing adjacency matrix for graph.
        - `degree_nodes(self, adjacency_matrix)`: computing the degree for each node.
        - `compute_laplacian_matrix(self, )`: computing the the Laplacian matrix for graph.


3. Support functions:

    - `get_log(message, log_type='INFO')`: module to return log message including the log type and time execute and message.

    - `save_path(path: list, file_name=None, mode='stdout')`: module writing path to screen or to file.


## How to run this project

1. After clone this repository, you change directory to src

```
cd src
```

2. Testing graph partition algorithms

Graph partition algorithm based on Breadth First Search

```
python main.py --number_nodes 20 --edge_prob 0.5 --threshold 4 --algorithm bfs
```

Kerninghan-Lin (KL) algorithm

```
python main.py --number_nodes 20 --edge_prob 0.5 --algorithm kl
```

Fiduccia-Mattheyses (FM) algorithm

```
python main.py --number_nodes 20 --edge_prob 0.5 --algorithm fm
```

Spectral Bisection

```
python main.py --number_nodes 20 --edge_prob 0.5 --algorithm sb
```

Kerninghan-Lin (KL) algorithm optimized by connected components

```
python main.py --number_nodes 20 --edge_prob 0.5 --algorithm scc_kl
```

## References

[1] Andreev, Konstantin; Räcke, Harald (2004). Balanced Graph Partitioning. Proceedings of the Sixteenth Annual ACM Symposium on Parallelism in Algorithms and Architectures. Barcelona, Spain. pp. 120–124. 

[2] Kernighan, B. W.; Lin, Shen (1970). "An efficient heuristic procedure for partitioning graphs". Bell System Technical Journal. 49: 291–307. doi:10.1002/j.1538-7305.1970.tb01770.x

[3] Fiduccia; Mattheyses (1982). "A Linear-Time Heuristic for Improving Network Partitions". 19th Design Automation Conference: 175–181. doi:10.1109/DAC.1982.1585498. ISBN 0-89791-020-6. Retrieved 23 October 2013.

## About us

Our project includes three contributors:
- Tran Xuan Loc - 22C11064 - 22C11064@student.hcmus.edu.vn (For project 02 & 03, Thanks for his based coding)
- Nguyen Bao Long - 22C11065 - 22C11065@student.hcmus.edu.vn (For project 02, Thanks for his based coding)
- Le Nhut Nam - 22C11067 - 22C11065@student.hcmus.edu.vn (For project 03, Thanks for his based coding)
