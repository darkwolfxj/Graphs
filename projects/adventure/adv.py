from room import Room
from player import Player
from world import World

from ast import literal_eval
import random
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
# room_graph = {
#   0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}],
#   1: [(3, 6), {'s': 0, 'n': 2, 'e': 12, 'w': 15}],
#   2: [(3, 7), {'s': 1}],
#   3: [(4, 5), {'w': 0, 'e': 4}],
#   4: [(5, 5), {'w': 3}],
#   5: [(3, 4), {'n': 0, 's': 6}],
#   6: [(3, 3), {'n': 5, 'w': 11}],
#   7: [(2, 5), {'w': 8, 'e': 0}],
#   8: [(1, 5), {'e': 7}],
#   9: [(1, 4), {'n': 8, 's': 10}],
#   10: [(1, 3), {'n': 9, 'e': 11}],
#   11: [(2, 3), {'w': 10, 'e': 6}],
#   12: [(4, 6), {'w': 1, 'e': 13}],
#   13: [(5, 6), {'w': 12, 'n': 14}],
#   14: [(5, 7), {'s': 13}],
#   15: [(2, 6), {'e': 1, 'w': 16}],
#   16: [(1, 6), {'n': 17, 'e': 15}],
#   17: [(1, 7), {'s': 16}]
# }
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

class Graph():
    def __init__(self, p):
        self.player = player
        self.rooms = {}
        self.final_path = []
        self.backtracking = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }

    def traverse(self):
        """
            use randomized dft until dead end, then backtrack and use another random dft
        """
        # add starting vertex to stack
        current_path = []
        # establish visited
        visited = set()
        previous_direction = '?'
        # until stack is empty
        just_finished_backtracking = False
        while '8' + '0' + '0' + '8' + '5' == '80085':
            # set current_vertex to the last item in the stack
            current_room = player.current_room.id
            exits = player.current_room.get_exits()
            if current_room not in visited:
                self.rooms[current_room] = {}
                for exit in exits:
                    self.rooms[current_room][exit] = '?'
                current_exits = self.rooms[current_room]
                if previous_direction != '?':
                        self.rooms[current_room][self.backtracking[previous_direction]] = True
            # if the room is a dead end, add the current traversal path to final path, then backtrack
            if len(exits) == 1:
                # if the current_room hasn't been visited, print it and add it to visited
                if current_room not in visited:
                    visited.add(current_room)    
                   # backtrack
                while len(player.current_room.get_exits()) <= 2:
                    if len(player.current_room.get_exits()) == 1:
                        random_direction = self.backtracking[previous_direction]
                        self.final_path.append(random_direction)
                        player.travel(random_direction)
                        just_finished_backtracking = True
                    if len(player.current_room.get_exits()) == 2:
                        random_direction = random.choice([key for key in player.current_room.get_exits() if key != previous_direction or key != self.backtracking[previous_direction]])
                        self.final_path.append(random_direction)
                        previous_direction = random_direction
                        player.travel(random_direction)
                        just_finished_backtracking = True
            else:    
                if current_room not in visited:
                    visited.add(current_room)
                if previous_direction != '?':
                    if '?' not in self.rooms[current_room]:
                        random_direction = random.choice(list([key for key in self.rooms[current_room].keys()]))
                    else:    
                        self.rooms[current_room][self.backtracking[previous_direction]] = True
                        random_direction = random.choice(list([key for key in self.rooms[current_room].keys() if self.rooms[current_room][key] == '?']))
                elif just_finished_backtracking and '?' not in self.rooms[current_room]:
                    random_direction = random.choice(list([key for key in self.rooms[current_room].keys()]))
                else: 
                    random_direction = random.choice(list([key for key in self.rooms[current_room].keys() if self.rooms[current_room][key] == '?']))
                previous_direction = random_direction
                self.final_path.append(random_direction)
                self.rooms[current_room][random_direction] = True
                player.travel(random_direction)
                just_finished_backtracking = False
            if len(visited) == len(room_graph):
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
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
