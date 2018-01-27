from itertools import permutations

class HanoiEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.curState = [0, 0, 0]
        self.action_space = list(permutations(range(3), 2))
        self.stepsDone = 0
    
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
