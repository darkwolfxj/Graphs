"""Given an object/dictionary with keys and values that consist of both strings and integers, design an algorithm to calculate and return the sum of all of the numeric values.
For example, given the following object/dictionary as input:
{
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}
Your algorithm should return 41, the sum of the values 23 and 18.
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process."""

# Iterate through the key/value pairs and append any integer value to a sum list
# return the sum of that list

def sumofints(d):
    ans = []
    for key, value in d.items():
        if type(value) == int:
            ans.append(value)
    return sum(ans)
    
correct = sumofints({
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
})
print(correct)

def dfs_recursive(self, starting_vertex, destination_vertex, visited=[]):
    """
    Return a list containing a path from
    starting_vertex to destination_vertex in
    depth-first order.

    This should be done using recursion.
    """
    # end case: if starting_vertex == destination_vertex return visited + current vertex (starting_vertex)
    if starting_vertex == destination_vertex:
        return visited + [starting_vertex]
    else:
        # while current vertex (starting_vertex) != destination vertex
        # append it to visited
        visited.append(starting_vertex)
        # add neighbors to path recursively, removing neighbors that don't lead to destination_vertex
        for neighbor in self.get_neighbors(starting_vertex):
            # if neighbor hasn't been visited
            if neighbor not in visited:
                # get path recursively
                path = self.dfs_recursive(neighbor, destination_vertex, visited)
                if path:
                    # if no longer recusing, return path
                    return path
        # if a path doesn't lead to destination_vertex, remove vertices until back on track             
        visited.remove(starting_vertex)
    
