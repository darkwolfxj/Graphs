from graph import Graph
from util import Stack
def earliest_ancestor(ancestors, starting_node=None):
    # index ancestors
    index = {}
    # creat an empty index
    for ancestor in ancestors:
        index[ancestor[1]] = []
    # for each ancestor in the index, add its ancestors
    for ancestor in ancestors:
        index[ancestor[1]].append(ancestor[0])
    # print(index)
    # create a graph with ancestors
    # preform a dft and save the paths yields, starting at the starting_node
    # if path return the smallest path[-1] from the largest path(s) else return -1  
    g = Graph()
    for ancestor in index:
        g.add_vertex(ancestor)
        for vertex in index[ancestor]:
            if vertex not in g.vertices:
                g.add_vertex(vertex)    
            g.add_edge(ancestor, vertex)
    print(g.dft_y_a(starting_node))
    return g.dft_y_a(starting_node)      
earliest_ancestor([(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)], 1)
