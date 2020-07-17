from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph():
    def __init__(self, player):
        self.player = player
        # establish a stack of traveresed rooms
        self.traversed = Stack()
        self.directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        self.rooms = {}
        self.final_path = []

    def traverse(self):
        # for each room, starting at the starting room (player.current_room.id), we need to index the neighboring rooms and add the directions traveled to reach them, plus the backtracking after reaching a room with no neighbors
        
        # the rooms neighboring the starting room are indexed
        self.rooms[self.player.current_room.id] = {}
        for direction in self.player.current_room.get_exits():
            # currently, no neighboring room is known
            self.rooms[self.player.current_room.id][direction] = 'unknown'
            
        # initiate a traveral loop with while True
        while True:
            # keep track of rooms that have never been visited, then visit them
            never_visited = []
           
            for room in self.rooms[self.player.current_room.id]:
                if self.rooms[self.player.current_room.id][room] == 'unknown':
                    # append all unvisited rooms to the never_visited list
                    never_visited.append(room)
            
            if len(never_visited) > 0:
                new_direction = never_visited.pop()
                self.traversed.push(self.directions[new_direction])
                # Mark the room as visited
                self.rooms[self.player.current_room.id][new_direction] = True
                # push the travelled direction to the stack 
                self.traversed.push(self.directions[new_direction])  
                # travel in the direction
                self.player.travel(new_direction)
                # append the travelled direction to the final path
                self.final_path.append(new_direction)
                
                # if the current_room isn't indexed, index it
                if player.current_room.id not in self.rooms:
                    self.rooms[self.player.current_room.id] = {}
                    
                    for direction in self.player.current_room.get_exits():
                        self.rooms[player.current_room.id][direction] = 'unvisited'
                    self.rooms[player.current_room.id][self.directions[direction]] = True
                    
            else:
                if self.traversed.size() > 0:
                    new_direction = self.traversed.pop()
                    self.player.travel(new_direction)
                    self.final_path.append(new_direction)
                else:
                    print(self.final_path)
                    return self.final_path



player = Player(world.starting_room)
graph = Graph(player)
traversal_path = graph.traverse()



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")