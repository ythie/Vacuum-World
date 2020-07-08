# This file contains the program for a vacuum agent in a continuum vacuum world

import random


class ContinuumWorld:
    """
    This class represents the observable world at any given instance.
    It contains functions for performing an action and printing the world grid.
    """

    def __init__(self, grid_size=[2, 2], dirt=[[1, 1], [1, 1]]):
        """This function will initialize an object for the ContinuumWorld class.

        Args:
            grid_size (list, optional): a list [x,y] with size of the world.
             Defaults to [2, 2].
            dirt (list, optional): a list of lists representing the entire
            world with the dirt value of each tile. Defaults to [[1, 1],[1, 1]].
        """
        self.grid_size = grid_size
        self.dirt = dirt

    def print_dirt(self, agent, position):
        """This function prints the current world representation with dirt in
        each tile

        Args:
            agent (Agent): the vacuum agent object,
            position (list): the current position of agent
        """
        # print(agent.position)
        part = self.dirt[:agent.position[0]]
        print()
        for row in part:
            print(*row, sep=", ")

        current = self.dirt[agent.position[0]]
        print(*current[:agent.position[1]], sep=", ", end=" ")
        print("["+str(self.dirt[agent.position[0]][agent.position[1]])
              + "]", end=" ")
        print(*current[agent.position[1]+1:], sep=", ")

        part = self.dirt[agent.position[0]+1:]
        for row in part:
            print(*row, sep=", ")
        print()


class Agent:
    """
    This class is for the basic description of the vacuum agent.
    It contains functions for verifying that it does not cross boundary,
    performing a moving or sucking action, and getting neighbor with maximum
    dirt.
    """

    def __init__(self, position=[0, 0], max_moves=30, grid_size=0, dirt=0):
        """This function will initialize an object for the Agent class

        Args:
            position (list, optional): the initial position of agent.
            Defaults to [0, 0].
            max_moves (int, optional): the maximum number of moves agent is
            allowed to take. Defaults to 30.
            grid_size (int, optional): a list [x,y] with size of the world.
            Defaults to 0.
            dirt (int, optional): a list of lists representing the entire
            world with the dirt value of each tile. Defaults to 0.
        """
        self.score = 0
        self.position = position
        self.max_moves = max_moves
        self.world = ContinuumWorld(grid_size, dirt)
        self.visited = set()
        self.visited.add((self.position[0], self.position[1]))

    def crosses_boundary(self, step):
        """This function checks if step taken by the agent will cross boundary.

        Args:
            step (String): any one from 'R', 'L', 'U' and 'D'

        Returns:
            boolean: True if boundary will be crossed
        """
        # error = "Cannot go beyond! Change direction!\n"
        if step == 'R':
            if self.position[1]+1 > self.world.grid_size[1]-1:
                # print(error)
                return True
        if step == 'L':
            if self.position[1]-1 < 0:
                # print(error)
                return True
        if step == 'U':
            if self.position[0]-1 < 0:
                # print(error)
                return True
        if step == 'D':
            if self.position[0]+1 > self.world.grid_size[0]-1:
                # print(error)
                return True

        return False

    def perform_action(self, action):
        """This function will change the position of the agent when movement
        actions are performed, and will change the tile to clean on suck action

        Args:
            action (String): the action to be performed
        """
        if action == 'R':
            self.position[1] += 1
        if action == 'L':
            self.position[1] -= 1
        if action == 'U':
            self.position[0] -= 1
        if action == 'D':
            self.position[0] += 1
        if action == 'S':
            self.score += self.world.dirt[self.position[0]][self.position[1]]
            self.world.dirt[self.position[0]][self.position[1]] = 0

        self.visited.add((self.position[0], self.position[1]))

    def print_status(self, step, counter=0):
        """This function prints the step and performance measure of agent at
        every step, and prints the world grid with current position of agent
        at every 5 steps.

        Args:
            step (String): direction or suck action taken by agent
            counter (int): counts the number of steps completed by agent
        """
        print(step, round(self.score, 5))
        # print(self.visited)
        if counter % 5 == 0:
            self.world.print_dirt(self, self.position)


class SimpleReflexAgent(Agent):
    """This reflex agent has no memory, no state and can only sense the present
    tile. It can sense the value of dirt present in and also if any of the
    boundary edges are walls.
    It has functions for moving aroud cleaning the world.

    Args:
        Agent (Agent): The parent class
    """

    def clean_grid(self):
        """This function is to tell the agent to move around and clean the
        tiles.
        """
        for i in range(self.max_moves):
            if self.world.dirt[self.position[0]][self.position[1]] > 0:
                step = 'S'
            else:
                while(True):
                    step = random.choice(['R', 'L', 'U', 'D'])
                    if self.crosses_boundary(step):
                        continue
                    else:
                        break

            self.perform_action(step)
            # print("Step number:", i)
            self.print_status(step, i)


class GreedyAgent(Agent):
    """This reflex agent has no memory, no state and can sense its
    neighboring tiles. It can sense the value of dirt present in and also if
    any of the boundary edges are walls.
    It contains functions for moving aroud cleaning the world.

    Args:
        Agent (Agent): The parent class
    """

    def clean_grid(self):
        """This function is to tell the agent to move around and clean the
        tiles.
        """
        for i in range(self.max_moves):
            if self.world.dirt[self.position[0]][self.position[1]] > 0:
                step = 'S'
            else:
                step = self.get_max_neighbor()

            self.perform_action(step)
            # print("Step number:", i)
            self.print_status(step, i)

    def get_max_neighbor(self):
        """This function checks which neighboring tile of agent has maximum
        dirt.

        Returns:
            String: the neighbor with maximum dirt value
        """
        neighbor = {}
        y = self.position[0]
        x = self.position[1]
        if not self.crosses_boundary('R'):
            neighbor['R'] = self.world.dirt[y][x+1]
        if not self.crosses_boundary('L'):
            neighbor['L'] = self.world.dirt[y][x-1]
        if not self.crosses_boundary('U'):
            neighbor['U'] = self.world.dirt[y-1][x]
        if not self.crosses_boundary('D'):
            neighbor['D'] = self.world.dirt[y+1][x]

        keys = list(neighbor.keys())
        random.shuffle(keys)
        neighbor = dict([(key, neighbor[key]) for key in keys])
        return max(neighbor, key=neighbor.get)


class StateAgent(Agent):
    """This reflex agent has memory, state and can sense its neighboring tiles.
    It can sense the value of dirt present in and also if any of the boundary
    edges are walls.
    It contains functions for moving aroud cleaning the world.

    Args:
        Agent (Agent): The parent class
    """

    def clean_grid(self):
        """This function is to tell the agent to move around and clean the
        tiles.
        """
        for i in range(self.max_moves):
            if self.world.dirt[self.position[0]][self.position[1]] > 0:
                step = 'S'
            else:
                step = self.get_best_neighbor()

            self.perform_action(step)
            # print("Step number:", i)
            self.print_status(step, i)

    def get_best_neighbor(self):
        """This function checks which neighboring tile of agent has maximum dirt
        and if that tile has been visited before.

        Returns:
            String: the neighbor with maximum dirt value
        """
        neighbor = {}
        y = self.position[0]
        x = self.position[1]

        flag = True
        if (not self.crosses_boundary('R')) and ((y, x+1) not in self.visited):
            flag = False
            neighbor['R'] = self.world.dirt[y][x+1]
        if (not self.crosses_boundary('L')) and ((y, x-1) not in self.visited):
            flag = False
            neighbor['L'] = self.world.dirt[y][x-1]
        if (not self.crosses_boundary('U')) and ((y-1, x) not in self.visited):
            flag = False
            neighbor['U'] = self.world.dirt[y-1][x]
        if (not self.crosses_boundary('D')) and ((y+1, x) not in self.visited):
            flag = False
            neighbor['D'] = self.world.dirt[y+1][x]
        if flag:
            while(True):
                step = random.choice(['R', 'L', 'U', 'D'])
                if self.crosses_boundary(step):
                    continue
                else:
                    break
            return step

        keys = list(neighbor.keys())
        random.shuffle(keys)
        neighbor = dict([(key, neighbor[key]) for key in keys])
        return max(neighbor, key=neighbor.get)


def read_file(text_file):
    """This function reads the 'environ.txt' file to retrieve initital state of
    world and agent.

    Args:
        text_file (file): the text file to fetch the information from

    Returns:
        pos [list]: the initial position of agent
        moves [int]: the maximum number of moves agent is allowed to take
        grid [list]: a list [x,y] with size of the world
        dirt [list[list[]]]: a list representing the entire world with the dirt
        value of eachtile
    """
    with open(text_file, 'r') as ev:
        e = ev.readlines()

    grid = []
    for i in e[0][e[0].find('GRID')+5:e[0].find('GRID')+10].split():
        grid.append(int(i))

    dirt = e[2:2+grid[0]]
    dirt = [[float(num) for num in row.split(' ')] for row in dirt]

    moves = int(e[10].replace('MOVES: ', ''))

    pos = []
    for i in e[11][e[11].find('INITIAL')+8:e[0].find('GRID')+15].split():
        pos.append(int(i)-1)

    # print(grid)
    # for row in dirt:
    #     print(row)
    # print(moves)
    # print(pos)

    return pos, moves, grid, dirt


def main():

    seed = 1  # for passing same random parameters to all three agents

    pos, moves, grid, dirt = read_file('environ.txt')
    # pos = [6, 0]
    random.seed(seed)
    reflex_agent = SimpleReflexAgent(pos, moves, grid, dirt)
    print("**Simple Reflex Agent**\n")
    reflex_agent.clean_grid()

    pos, moves, grid, dirt = read_file('environ.txt')
    # pos = [6, 0]
    random.seed(seed)
    greedy_agent = GreedyAgent(pos, moves, grid, dirt)
    print("\n**Greedy Agent**\n")
    greedy_agent.clean_grid()

    pos, moves, grid, dirt = read_file('environ.txt')
    # pos = [6, 0]
    random.seed(seed)
    state_agent = StateAgent(pos, moves, grid, dirt)
    print("\n**State Agent**\n")
    state_agent.clean_grid()


if __name__ == "__main__":
    main()
