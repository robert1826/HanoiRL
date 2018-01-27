from hanoiEnv import HanoiEnv
import random

random.seed(42)

def genSession(env=HanoiEnv()):
    s = env.reset()

    # results 
    stateList = []
    actionList = []
    totalReward = 0
    
    while 1:
        a = random.choice(env.action_space)
        print('picked action', a)

        stateList += [s]
        actionList += [a]

        s, r, done = env.step(a)
        print('resulted state', s)

        totalReward += r
        if done:
            print('Done with overall reward =', totalReward, 'in #steps =', env.stepsDone)
            break
    
    return stateList, actionList, totalReward

if __name__ == '__main__':
    genSession()