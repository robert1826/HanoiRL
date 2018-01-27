from hanoiEnv import HanoiEnv
import random

random.seed(42)

def genSession(env=HanoiEnv()):
    s = env.reset()
    all_r = 0
    while 1:
        a = random.choice(env.action_space)
        print('picked action', a)

        s, r, done = env.step(a)
        print('resulted state', s)

        all_r += r
        if done:
            print('Done with overall reward =', all_r, 'in #steps =', env.stepsDone)
            break

if __name__ == '__main__':
    genSession()