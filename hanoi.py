class HanoiEnv:
    def __init__(self):
        self.state = [0, 0, 0]
    
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

env = HanoiEnv()
s = env.decodeState([0, 0, 0])
print(s)
s = env.encodeState(s)
print(s)