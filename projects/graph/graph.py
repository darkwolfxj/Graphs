"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1].add(v2)
    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # establish a queue
        q = Queue()
        # add starting vertex to queue
        q.enqueue([starting_vertex])
        # create a set of vertexes visited
        visited = set()
        # until queue is empty
        while q.size() > 0:
            # set current_vertex to the first item in the queue
            path = q.dequeue()
            current_vertex = path[-1] 
            if current_vertex not in visited:
                # if the current_vertex hasn't been visited, print it and add it to visited
                print(current_vertex)
                visited.add(current_vertex)
                # enqueue all of the neighbors
                for vertex in self.get_neighbors(current_vertex):
                    new_path = path + [vertex]
                    q.enqueue(new_path)
    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # establish a stack
        s = Stack()
        # add starting vertex to stack
        s.push(starting_vertex)
        # create a set of vertexes visited
        visited = set()
        # until stack is empty
        while s.size() > 0:
            # set current_vertex to the last item in the stack
            current_vertex = s.pop()
            if current_vertex not in visited:
                # if the current_vertex hasn't been visited, print it and add it to visited
                print(current_vertex)
                visited.add(current_vertex)
                # add all of the neighbors to the stack
                for vertex in self.get_neighbors(current_vertex):
                    s.push(vertex) 
  
    def dft_recursive_utils(self, v, visited):
        # add a the vertex to the visited set and print it
        visited[v[-1]] = True
        print(v[-1])
        # if it's been visited, don't do anything 
        for vertex in self.get_neighbors(v[-1]):
            if visited[vertex] == False:
        # otherwise, plug neighbors into recursion
                self.dft_recursive_utils(v + [vertex], visited)
    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # created a False entry for all vertexes
        visited = {}
        for vertex in self.vertices:
            visited[vertex] = False
        # print(visited)       
        self.dft_recursive_utils([starting_vertex], visited)
    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
       # establish a queue
        q = Queue()
        # add starting vertex to queue
        q.enqueue([starting_vertex])
        # create a set of vertexes visited
        visited = set()
        # until queue is empty
        while q.size() > 0:
            # set current_vertex to the first item in the queue
            path = q.dequeue()
            current_vertex = path[-1] 
            if current_vertex not in visited:
                # if the current_vertex hasn't been visited, print it and add it to visited
                visited.add(current_vertex)
                # enqueue all of the neighbors
                for vertex in self.get_neighbors(current_vertex):
                    new_path = path + [vertex]
                    q.enqueue(new_path)
            if current_vertex == destination_vertex:
                return path
                
    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
       # establish a stack
        s = Stack()
        # add starting vertex to stack
        s.push([starting_vertex])
        # create a set of vertexes visited
        visited = set()
        # until stack is empty
        while s.size() > 0:
            # set current_vertex to the first item in the stack
            path = s.pop()
            current_vertex = path[-1] 
            if current_vertex not in visited:
                # if the current_vertex hasn't been visited, print it and add it to visited
                visited.add(current_vertex)
                # enqueue all of the neighbors
                for vertex in self.get_neighbors(current_vertex):
                    new_path = path + [vertex]
                    s.push(new_path)
            if current_vertex == destination_vertex:
                return path 
                   
    def dfs_recursive_utils(self, v, visited, destination_vertex, finalanswer=False):
        
            # add a the vertex to the visited set and print it
        visited[v[-1]] = True
        # if it's been visited, don't do anything 
        if v[-1] == destination_vertex:
            finalanswer = v
            return v
        elif v[-1] != destination_vertex:
            for vertex in self.get_neighbors(v[-1]):
                if visited[vertex] == False:
                # otherwise, plug neighbors into recursion
                    result = self.dfs_recursive_utils(v + [vertex], visited, destination_vertex, )
                    if result:
                        return result
    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # created a False entry for all vertexes
        visited = {}
        for vertex in self.vertices:
            visited[vertex] = False
        # print(visited)       
        return self.dfs_recursive_utils([starting_vertex], visited, destination_vertex)

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    # print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
    print(dir(Graph))