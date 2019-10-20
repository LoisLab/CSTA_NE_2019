#@title (run this cell to load machine learning environment) { vertical-output: true, display-mode: "form" }
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

class Maze():
    # nicknames for actions... for beginners, only
    actions = ['N','S','E','W']
    # offsets to move North, South, East, or West
    offset = [(0,-1),(0,1),(1,0),(-1,0)]

    def __init__(self):
        self.mark = None
        self.reset()

    def reset(self, random=False):
        self.maze = np.array([[0,0,0,-1],[0,-1,0,-1],[0,0,-1,0],[-1,0,0,0]])  # the maze is hardcoded
        self.i = 1
        self.maze[0][0] = self.i  # mark initial position with counter
        self.player = (0,0)
        return self.player

    # action should be one of: 'N', 'S', 'E', 'W'
    # returns reward, done
    # rewards are: +1 = success, -1 = failure, 0 = no outcome
    # done = True if a terminal state is reached, otherwise False
    def step(self, action):
        self.i += 1
        if type(action) is str:
            action = Maze.actions.index(action)
        self.player = tuple(np.add(self.player, Maze.offset[action]))
        if max(self.player) > 3 or min(self.player) < 0:        # out of bounds
            return self.player, -1, True
        else:
            if self.maze[self.player[0]][self.player[1]] == -1: # moved onto a blocked space
                return self.player, -1, True
            self.maze[self.player[0]][self.player[1]] = self.i
            if np.array_equal(self.player, (3,3)):              # reached the exit
                return self.player, 1, True
            else:
                return self.player, 0, False                    # no outcome (player is on an open space)

    # return a random action (equally distributed across the action space)
    def sample(self):
        return Maze.actions[np.random.randint(4)]

    # return a random action in numeric form (equally distributed across the action space)
    def sample_n(self):
        return np.random.randint(4)

    def action_space(self):
        return Maze.actions
    
    def action_space_n(self):
        return [0,1,2,3]

    def state_space(self):
        return 4,4

    def __str__(self):
        out = '\n=========='  
        for y in range(4):
            out += '\n|'
            for x in range(4):
                if self.mark is not None and self.mark[0]==x and self.mark[1]==y:
                    out += '? '
                elif self.maze[x][y]>0:
                    out += str(self.maze[x][y]) + ' '
                elif self.maze[x][y]==-1:
                    out += 'X '
                elif x==3 and y==3:
                    out += '* '
                else:
                    out += '. '
            out += '|'
        out += '\n==========\n'
        return out                     
 
    def print_q(q, mode='all'):
        print('=====  ================================')
        print('state         N       S       E       W\n')
        for x in range(4):
            for y in range(4):
                out = '('
                out += str(x)
                out += ','
                out += str(y)
                out += ')  '
                for a in range(4):
                    if mode=='all':
                        out += '{:>8,d}'.format(int(q[x][y][a]))
                    elif mode=='rewards':
                        if q[m][n][a] > 0:
                            out += '{:8.3f}'.format(q[x][y][a])
                        else:
                            out += '        '
                print(out)
            print('-----  --------------------------------')

    def plot(q):
      fig = plt.figure(figsize=(16,6))
      ax1 = fig.add_subplot(121, projection='3d')
      x,y,b = [],[],[]
      z = np.zeros((4,4))
      for m in range(4):
        for n in range(4):
          x.append(m)
          y.append(n)
          b.append(0)
          z[m][n] += max(max(q[m][n]),0)
            
      ax1.bar3d(x, y, b, 1, 1, np.ravel(z), shade=True)
      plt.title('Positive Q-scores')
      plt.xlabel('state (row)')
      plt.ylabel('state (col)')
      plt.show()

print('the maze environment is all set to go')
