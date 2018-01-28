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
        a = stateEnc.transform([s])
        a = agent.predict_proba(a).reshape(-1)
        a = np.random.choice(len(env.action_space), p=a)

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
    return a

if __name__ == '__main__':
    BatchSize = 50
    percentile = 70 #fit on top 30% (30 best samples)
    NEpisodes = 100

    # init env
    env = HanoiEnv()

    dummyStates = [[0, 0, 0], [0, 1, 2], [2, 1, 0]] * 2
    dummyActions = env.action_space

    # init stateEnc
    stateEnc = OneHotEncoder(n_values=3, dtype=type(1), sparse=False)
    stateEnc.fit(dummyStates)

    # # init model
    agent = MLPClassifier(max_iter=1, warm_start=True)
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

        # convert elite_action back to a list of tuples 
        elite_actions = elite_actions.tolist()
        elite_actions = [tuple(i) for i in elite_actions]

        agent.fit(stateEnc.transform(elite_states), oneHotEncodeActions(elite_actions, len(env.action_space)))
        
        #report progress
        print("epoch %i \tmean reward=%.2f\tthreshold=%.2f"%(i, batch_rewards.mean(), threshold))