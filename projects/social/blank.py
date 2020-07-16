import random
from itertools import permutations
from util import Stack, Queue
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
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
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
        ## use num_users
        user_ids = []
        for user in range(num_users + 1):
            self.add_user(random.randint(1, num_users * 100))
        for user in self.users:
            user_ids.append(user)
        perms = list(permutations(user_ids, 2))
        final_list = random.sample(perms, num_users * avg_friendships // 2)
        for pair in final_list:
            self.add_friendship(pair[0], pair[1])
    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        paths = []
        for friend in self.get_friendships(user_id):
            paths.append(self.dft_search(friend))
        extended_network = []
        for path in paths:
            for i in path:
                for j in i:
                    if j not in extended_network:
                        extended_network.append(j)
        extended_network_paths = []
        for end_user_id in extended_network:
            extended_network_paths.append(self.bft_search(user_id, end_user_id))
        print(extended_network_paths)
        for i in extended_network_paths:
            for extended_network in i:
                visited[extended_network[-1]] = extended_network
        return visited
    def get_friendships(self, user_id):
        return self.friendships[user_id]
    def dft_search(self, user_id):
        # returns extended network
        s = Stack()
        visited = {}
        connections = []
        if s.size() == 0:
            s.push([user_id])
        while s.size() > 0:
            current_path = s.pop()
            current_user_id = current_path[-1]
            if current_user_id not in visited:
                visited[current_user_id] = current_path
            if len(self.get_friendships(current_user_id)) == 1:
                connections.append(current_path)
            else:
                for friend in self.get_friendships(current_user_id):
                    if friend not in visited:
                        visited[friend] = current_path + [friend]
                        s.push(current_path + [friend])
        return connections
    def bft_search(self, start_user_id, end_user_id):
        # return shortest path
        q = Queue()
        visited = set()
        connections = []
        q.enqueue([start_user_id])
        while q.size() > 0:
            current_path = q.dequeue()
            current_user_id = current_path[-1]
            if current_user_id not in visited:
                visited.add(current_user_id)
                for friend_of_friend in self.get_friendships(current_user_id):
                    new_path = current_path + [friend_of_friend]
                    q.enqueue(new_path)
            if current_user_id == end_user_id:
                connections.append(current_path)
        shortest_path = [path for path in connections if len(path) == min(len(x) for x in connections)]
        return shortest_path
if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)