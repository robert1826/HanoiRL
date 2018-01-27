from hanoiEnv import HanoiEnv
import random
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder, label_binarize

random.seed(42)
np.random.seed(31)

def genSession(env, agent, stateEnc, verbose=False):
    env.reset()
    s = env.curState

    # results 
    stateList = []
    actionList = []
    totalReward = 0
    
    while 1:
        a = agent.predict(stateEnc.transform([s]))[0]
        if verbose:
            print('predicted', a)
            
        a = env.action_space[a]
        if verbose:
            print('predicted action', a)

        stateList += [s]
        actionList += [a]

        s, r, done = env.step(a)
        if verbose:
            print('resulted state', s)

        totalReward += r
        if done:
            if verbose:
                print('Done with overall reward =', totalReward, 'in #steps =', env.stepsDone)
            break
    
    return stateList, actionList, totalReward

def oneHotEncodeActions(actions, nFeatures):
    a = [env.action_space.index(i) for i in actions]
    # return np.eye(nFeatures)[a]
    return a

    ##### alternate implementation
    
    # a = [env.action_space.index(i) for i in actions]
    # a = np.array(a)
    # b = np.zeros((len(a), nFeatures))
    # b[np.arange(len(a)), a] = 1
    # return b

if __name__ == '__main__':
    BatchSize = 100
    percentile = 70 #fit on top 30% (30 best samples)
    NEpisodes = 100

    dummyStates = [[0, 0, 0], [0, 1, 2], [2, 1, 0]]
    dummyActions = [(0, 1), (2, 1), (0, 2)]

    # init env
    env = HanoiEnv()

    # init stateEnc
    stateEnc = OneHotEncoder(n_values=3, dtype=type(1), sparse=False)
    stateEnc.fit(dummyStates)

    # # init model
    agent = MLPClassifier(max_iter=1)
    x = stateEnc.transform(dummyStates)
    y = oneHotEncodeActions(dummyActions, len(env.action_space))
    agent.fit(x, y)

    for i in range(NEpisodes):
        sessions = [genSession(env, agent, stateEnc) for _ in range(BatchSize)]

        batch_states, batch_actions, batch_rewards = map(np.array, zip(*sessions))

        # pick elite sessions
        threshold = np.percentile(batch_rewards, percentile)
        elite_states = np.concatenate(batch_states[batch_rewards >= threshold])
        elite_actions = np.concatenate(batch_actions[batch_rewards >= threshold])

        agent.fit(stateEnc.transform(elite_states), oneHotEncodeActions(elite_actions, len(env.action_space)))
        
        #report progress
        print("epoch %i \tmean reward=%.2f\tthreshold=%.2f"%(i, batch_rewards.mean(), threshold))