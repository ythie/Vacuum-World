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


class SimpleReflexAgent:
    '''
    This class is for the functions of the vacuum agent.
    It contains functions for verifying that it does not cross boundary and for
    cleaning the world.
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
        self.max_moves = 30
        self.world = ContinuumWorld(grid_size, dirt)

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


def main():

    pos, moves, grid, dirt = read_file('environ.txt')

    agent = SimpleReflexAgent(pos, moves, grid, dirt)
    agent.clean_grid()


if __name__ == "__main__":
    main()
