# This file contains the program for a vacuum agent in a continuum vacuum world

import random


class ContinuumWorld:
    '''
    This class represents the observable world at any given instance.
    It contains functions for performing an action and printing the world grid.
    '''

    def __init__(self, grid_size=[2, 2], dirt=[[1, 1], [1, 1]]):
        '''
        This function will initialize an object for the ContinuumWorld class.
        Arguments:
            grid_size - a list [x,y] with size of the world
            dirt - a list of lists representing the entire world with the dirt
            value
                of each tile
        '''
        self.grid_size = grid_size
        self.dirt = dirt

    def print_dirt(self, agent, position):
        '''
        This function prints the current world representation with dirt in each
        tile
        Arguments:
            agent - the vacuum agent object
            position - the current position of agent
        '''
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

    @classmethod
    def generate_world(cls):

        grid_size = [8,5]
        dirt = [[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])]

        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                if random.random()>0.5:
                    dirt[i][j]=round(random.random(),2)
                else:
                    dirt[i][j]=0.0

        return cls(grid_size,dirt)

class Agent:
    '''
    This class is for the basic description of the vacuum agent.
    It contains functions for verifying that it does not cross boundary,
    performing a moving or sucking action, and getting neighbor with maximum
    dirt.
    '''

    def __init__(self, position=[0, 0], max_moves=30, grid_size=0, dirt=0):
        '''
        This function will initialize an object for the SimpleReflexAgent class
        Arguments:
            position - the initial position of agent
            max_moves - the maximum number of moves agent is allowed to take
            grid_size - a list [x,y] with size of the world
            dirt - a list of lists representing the entire world with the dirt
            value of each tile
        '''
        self.score = 0
        self.position = position
        self.max_moves = max_moves
        self.world = ContinuumWorld(grid_size, dirt)
        self.visited = set()

    def crosses_boundary(self, step):
        '''
        This function checks if step taken by the agent will cross boundary.
        Arguments:
            step - any one from 'R', 'L', 'U' and 'D'
        Returns: True if boundary will be crossed
        '''
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
        '''
        This function will change the position of the agent when movement
        actions are performed, and will change the tile to clean on suck action
        Arguments:
            agent - the vacuum agent object
            action - the action performed
        '''
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

class SimpleReflexAgent(Agent):
    '''
    This reflex agent has no memory, no state and can only sense the present
    tile. It can sense the value of dirt present in and also if any of the
    boundary edges are walls.
    It contains functions for moving aroud cleaning the world.
    '''

    def clean_grid(self):
        '''
        This function is to tell the agent to move around and clean the tiles.
        '''
        counter = 0
        for i in range(self.max_moves):
            counter += 1
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
            # print("Step number:", counter)
            print(step, round(self.score, 5))

            if counter % 5 == 0:
            self.world.print_dirt(self, self.position)

class GreedyAgent(Agent):
    '''
    This reflex agent has no memory, no state and can sense its
    neighboring tiles. It can sense the value of dirt present in and also if
    any of the boundary edges are walls.
    It contains functions for moving aroud cleaning the world.
    '''

    def clean_grid(self):
        '''
        This function is to tell the agent to move around and clean the tiles.
        '''
        counter = 0
        for i in range(self.max_moves):
            counter += 1
            if self.world.dirt[self.position[0]][self.position[1]] > 0:
                step = 'S'
            else:
                step = self.get_max_neighbor()

            self.perform_action(step)
            # print("Step number:", counter)
            print(step, round(self.score, 5))

            if counter % 5 == 0:
            self.world.print_dirt(self, self.position)

    def get_max_neighbor(self):
        '''
        This function checks which neighboring tile of agent has maximum dirt.
        Return:
            direction in which maximum dirt is present, 'R', 'L', 'U' or 'D'
        '''
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

        itemMaxValue = max(neighbor.items(), key=lambda x: x[1])
        listOfKeys = list()

        for key, value in neighbor.items():
            if value == itemMaxValue[1]:
                listOfKeys.append(key)
        return random.choice(listOfKeys)

class StateAgent(Agent):
    '''
    This reflex agent has memory, state and can sense its neighboring tiles.
    It can sense the value of dirt present in and also if any of the boundary
    edges are walls.
    It contains functions for moving aroud cleaning the world.
    '''

    def clean_grid(self):
        '''
        This function is to tell the agent to move around and clean the tiles.
        '''
        counter = 0
        for i in range(self.max_moves):
            counter += 1
            if self.world.dirt[self.position[0]][self.position[1]] > 0:
                step = 'S'
            else:
                step = self.get_best_neighbor()

            self.perform_action(step)
            # print("Step number:", counter)
            print(step, round(self.score, 5))
            # print(self.visited)

            if counter % 5 == 0:
            self.world.print_dirt(self, self.position)

    def get_best_neighbor(self):
        '''
        This function checks which neighboring tile of agent has maximum dirt.
        Return:
            direction in which maximum dirt is present, 'R', 'L', 'U' or 'D'
        '''
        neighbor = {}
        y = self.position[0]
        x = self.position[1]
        Y = self.world.grid_size[0]
        X = self.world.grid_size[1]

        flag=True
        if (not self.crosses_boundary('R')) and ((y, x+1) not in self.visited):
            flag=False
            neighbor['R'] = self.world.dirt[y][x+1]
        if (not self.crosses_boundary('L')) and ((y, x-1) not in self.visited):
            flag=False
            neighbor['L'] = self.world.dirt[y][x-1]
        if (not self.crosses_boundary('U')) and ((y-1, x) not in self.visited):
            flag=False
            neighbor['U'] = self.world.dirt[y-1][x]
        if (not self.crosses_boundary('D')) and ((y+1, x) not in self.visited):
            flag=False
            neighbor['D'] = self.world.dirt[y+1][x]
        if flag:
            while(True):
                step = random.choice(['R', 'L', 'U', 'D'])
                if self.crosses_boundary(step):
                    continue
                else:
                    break
            return step

        itemMaxValue = max(neighbor.items(), key=lambda x: x[1])
        listOfKeys = list()

        for key, value in neighbor.items():
            if value == itemMaxValue[1]:
                listOfKeys.append(key)
        return random.choice(listOfKeys)


def read_file(text_file):
    '''
    This function reads the 'environ.txt' file to retrieve initital state of
    world and agent.
    Arguments:
        text_file - the text file to fetch the information from
    Returns:
        pos - the initial position of agent
        moves - the maximum number of moves agent is allowed to take
        grid - a list [x,y] with size of the world
        dirt - a list representing the entire world with the dirt value of each
            tile
    '''
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


def test():

    random.seed(1)
    reflex_total_score=0
    for i in range(1):
        #pos, moves, grid, dirt = read_file('environ.txt')
        random_world = ContinuumWorld.generate_world()
        reflex_agent = SimpleReflexAgent([2,4], 30, random_world.grid_size, random_world.dirt)
        reflex_agent.clean_grid()
        reflex_total_score+=reflex_agent.score

    random.seed(1)
    greedy_total_score=0
    for i in range(1):
        #pos, moves, grid, dirt = read_file('environ.txt')
        random_world = ContinuumWorld.generate_world()
        greedy_agent = GreedyAgent([2,4], 30, random_world.grid_size, random_world.dirt)
        greedy_agent.clean_grid()
        greedy_total_score+=greedy_agent.score

    random.seed(1)
    state_total_score=0
    for i in range(1):
        #pos, moves, grid, dirt = read_file('environ.txt')
        random_world = ContinuumWorld.generate_world()
        state_agent = StateAgent([2,4], 30, random_world.grid_size, random_world.dirt)
        state_agent.clean_grid()
        state_total_score+=state_agent.score

    print(reflex_total_score)
    print(greedy_total_score)
    print(state_total_score)

def main():

    random.seed(2)
    pos, moves, grid, dirt = read_file('environ.txt')
    reflex_agent = SimpleReflexAgent(pos, moves, grid, dirt)
    reflex_agent.clean_grid()

    random.seed(2)
    pos, moves, grid, dirt = read_file('environ.txt')
    greedy_agent = GreedyAgent(pos, moves, grid, dirt)
    greedy_agent.clean_grid()

    random.seed(2)
    pos, moves, grid, dirt = read_file('environ.txt')
    state_agent = StateAgent(pos, moves, grid, dirt)
    state_agent.clean_grid()

    print(reflex_agent.score)
    print(greedy_agent.score)
    print(state_agent.score)


if __name__ == "__main__":
    test()
