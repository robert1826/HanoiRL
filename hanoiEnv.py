from itertools import permutations

class HanoiEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.curState = [0, 0, 0]
        self.action_space = list(permutations(range(3), 2))
        self.stepsDone = 0
    
    def step(self, action_tuple=None, action_int=None):
        # action_tuple is a tuple with source and dest pile ind (ex. (1, 0))
        # action_int is an int which is the index of the action in self.action_space
        # only one of the above could be non-null

        action = action_tuple if action_tuple else self.action_space[action_tuple]
        src_pile = [i for i in range(3) if self.curState[i] == action[0]]
        dest_pile = [i for i in range(3) if self.curState[i] == action[1]]

        # check if valid action
        if len(src_pile) == 0 or src_pile[0] > dest_pile[0]:
            return self.curState, -100, False
        
        # results
        reward = 0
        done = False

        # actual step
        self.curState[src_pile[0]] = action[1]

        # check for end of episode
        new_dest_pile = [i for i in range(3) if self.curState[i] == action[1]]
        if new_dest_pile == list(range(3)):
            done = True

        return self.curState, reward, done
    
    def decodeState(self, s):
        res = [[], [], []]
        for i in range(3):
            res[i] = [j for j in range(3) if s[j] == i]
        return res
    
    def encodeState(self, s):
        res = []
        for i in range(3):
            res += [j for j in range(3) if i in s[j]]
        return res
