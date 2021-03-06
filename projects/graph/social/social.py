import random
import time


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(numUsers):
            self.addUser(f"User {i}")

        # Create friendships
        possibleFriendships = []
        for userID in self.users:
            for friendID in range(userID + 1, self.lastID + 1):
                possibleFriendships.append((userID, friendID))
            # the inside for loop matches with next userID, appends
            # to list, then adds one to both
            # this will eventually generate all the possible combinations
            # of friendships
        # print(f"poss friend before shuffle", possibleFriendships)
        # shuffle the friendships
        random.shuffle(possibleFriendships)
        # print(f"poss friend after shuffle", possibleFriendships)

        # now we iterate through the possible friendships array, apply the splice: formula
        for friendship in possibleFriendships[: (numUsers * avgFriendships) // 2]:
            # print(f"CREATING FRIENDSHIP: {friendship}")
            # add the friendship pair using the addFriendship method written at top
            self.addFriendship(friendship[0], friendship[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """

        # BFS
        queue = []
        visited = {}  # Note that this is a dictionary, not a set
        initial_list = [userID]  # adds first element to a list
        queue.append(initial_list)  # adds list to queue

        while queue:
            # initial value of q is a single element,
            # in the future it will hold lists
            # grab the last item in list
            # errors int not subscriptable. work around is to create an initial list container userID, then appending THAT to.

            # print(f"queue index 0: ", queue[0])
            # print(f"list before pop: ", queue)
            path = queue.pop(0)  # remove from index zero
            new_ID = path[-1]
            if new_ID not in visited:
                # each iteration we keep track of the node AND the path
                # we add the id, then have a corresponding path we want to
                # continue after it
                visited[new_ID] = path  # key = value {key: value}
                for friend in self.friendships[new_ID]:
                    if friend not in visited:
                        new_path = list(path)
                        new_path.append(friend)
                        queue.append(new_path)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    start_time = time.time()
    sg.populateGraph(1000, 5)
    end_time = time.time()
    print(f'runtime: {end_time - start_time} seconds')

    # print(f"friendships:", sg.friendships)
    connections = sg.getAllSocialPaths(1)
    # print(f"connections:", connections)

    # total = 0

    # for userID in connections:
    #     total += len(connections[userID]) - 1
    # print(len(connections))
    # print(total / len(connections))

    # totalConnections = 0
    # totalDegrees = 0
    # iterations = 10

    # for i in range(0, iterations):
    #     sg.populateGraph(1000, 5)
    #     connections = sg.getAllSocialPaths(1)
    #     total - 0

    #     for userID in connections:
    #         total += len(connections)
    #     totalConnections += len(connections)
    #     totalDegrees += total / len(connections)
    #     print("------")
    #     print(f"friends in network: {len(connections)}")
    #     print(f"Avg degrees: {total / len(connections)}")
    # print(totalConnections/iterations)
    # print(totalDegrees / iterations)
