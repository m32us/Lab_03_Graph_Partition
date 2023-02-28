# Lab_02_BFS_DFS

In this project, we implement Breadth First Search (BFS) and Depth Frist Search (DFS) based on the given structure of Graph.
	
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

3. Support functions:

    - `get_log(message, log_type='INFO')`: module to return log message including the log type and time execute and message.

    - `save_path(path: list, file_name=None, mode='stdout')`: module writing path to screen or to file.


## References
[1] MỘT SỐ BÀI TOÁN CƠ BẢN TRONG PHÂN TÍCH DỮ LIỆU. Thuc Nguyen Dinh. Ferbruary 27, 2023.

## About Us
Our project includes two contributors:
- Tran Xuan Loc - 22C11064 - 22C11064@student.hcmus.edu.vn
- Nguyen Bao Long - 22C11065 - 22C11067@student.hcmus.edu.vn
