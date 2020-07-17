from util import Stack, Queue
import random
from itertools import permutations
import time
class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            # print("WARNING: Cannot be friends with yourself!")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        # Add users
        # create an empty user_id list
        users = []        
        # generate random users
        for i in range(1, num_users + 1):
            self.add_user(random.randint(0, num_users**2))
        # Create friendships
        for user in self.users:
            # add users and their corresponding id's to the user_id list
            users.append((self.users[user].name, user))
        # generate all possible friendship combinations for each user
        possible_friendships = list(permutations(users, 2))
        # select a random sample of friendship configurations averaging to the selected number of friendships
        friendships_to_add = random.sample(possible_friendships, avg_friendships * num_users // 2)
        # add the friendships to the Social Graph
        for friendship in friendships_to_add:
            self.add_friendship(friendship[0][1], friendship[1][1])
            
    def get_friendships(self, user_id):
        return self.friendships[user_id]
    
    def dft_deepest_connection(self, user_id):
        # establish a list of paths
        connections = []
        # establish a stack
        s = Stack()
        # establish visited
        visited = {}
        # if stack is empty, populate it with the first path
        if s.size() == 0:
            s.push([user_id])
        # while stack is not empty, pop the first path
        while s.size() > 0:
            current_path = s.pop()
            current_user = current_path[-1]
            if current_user not in visited:
                visited[current_user] = current_path
            if len(self.get_friendships(current_user)) == 1:
                connections.append(current_path)
            else:
                for friend in self.get_friendships(current_user):
                    if friend not in visited:
                        new_path = current_path + [friend]
                        visited[friend] = new_path
                        # print("new path", new_path)
                        s.push(new_path)
        # print("visited: ", visited)
        # print("connections paths for ", user_id, connections)   
        return connections
    
    def shortest_path(self, start_user_id, end_user_id):
        paths = []
        q = Queue()
        # add starting vertex to queue
        q.enqueue([start_user_id])
        # create a set of vertexes visited
        visited = set()
        # until queue is empty
        while q.size() > 0:
            # set current_vertex to the first item in the queue
            path = q.dequeue()
            current_friend = path[-1] 
            if current_friend not in visited:
                # if the current_vertex hasn't been visited, print it and add it to visited
                visited.add(current_friend)
                # enqueue all of the neighbors
                for friend_of_friend in self.get_friendships(current_friend):
                    new_path = path + [friend_of_friend]
                    q.enqueue(new_path)
            if current_friend == end_user_id:
                paths.append(path)
        # print("paths in bfs", paths)
        # print("visited in bfs", visited)
        shortest_path = [path for path in paths if len(path) == min(len(x) for x in paths)]
        return shortest_path
        
    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        paths = []
        visited[user_id] = [user_id]
        # for each friend of the selected user
        for friend in self.get_friendships(user_id):
            paths.append(self.dft_deepest_connection(friend))
            # perform a dft and find the deepest path
            # visited[deepest_path[-1]] = custom_bft(user_id, deepest_path[-1]) 
            # return visited
            pass
        
        # print(self.friendships[user_id])
        extended_network = []
        for path in paths:
            for i in path:
                for j in i:
                    if j not in extended_network:
                        extended_network.append(j)
        # print("extended network", extended_network)
        all_extended_network_paths = []
        for friend in extended_network:
            all_extended_network_paths.append(self.shortest_path(user_id, friend))
        for i in all_extended_network_paths:
            for extended_network in i:
                visited[extended_network[-1]] = extended_network
            # print(extended_network_path)
            pass
        # print(all_extended_network_paths)
        return visited
    
    def linear_populate_graph(self, num_users, avg_friendships):
        generated_friendships = 0
        for user in range(num_users + 1):
            self.add_user(user)
        while generated_friendships < num_users * avg_friendships // 2:
            if self.add_friendship(random.randint(1, self.last_id), random.randint(1, self.last_id)):
                generated_friendships += 2

if __name__ == '__main__':
    sg = SocialGraph()
    num_users = 5000
    avg_friendships = 2
    start_time = time.time()
    sg.populate_graph(num_users, avg_friendships)
    end_time = time.time()
    print("finished")
    print(end_time - start_time)
    start_time = time.time()
    sg.linear_populate_graph(num_users, avg_friendships)
    end_time = time.time()
    print("finished again")
    print(end_time - start_time)
    # print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    # print(connections)
    
    avg_deg_of_sep = sum([len(connections[connection]) for connection in connections if len(connections[connection]) != 1])/len(connections)
    print(avg_deg_of_sep)
