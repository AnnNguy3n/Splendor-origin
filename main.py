from collections import Counter
import gym
import gym_splendor
import time
import copy

env = gym.make('gym_splendor-v0')
def main():
    env.reset()

    while env.turn < 400:
        # env.render()
        o,a,done,t = env.step(env.players[env.turn % env.amount_player].action(env.dict_input))
        if done == True:
            break

    # env.render()
    # print('----------------------------------------------------------------------------------------------------')

    for i in range(env.players.__len__()):
        env.dict_input['Players'] = [env.players[(j+1)%env.amount_player] for j in range(env.amount_player-1)]
        env.players[i].action(env.dict_input)
        env.render()
    
    _ = [p for p in env.players if p.score == env.board.current_highest_score]
    _t = [p.opened_cards.__len__() + p.upside_cards.__len__() for p in _]
    min_t = min(_t)
    for i in range(_t.__len__()-1, -1, -1):
        if _t[i] == min_t:
            print(_[i].name)
            return _[i].name

    print('None')
    return 'None'

a = time.time()
cnt = Counter(main() for i in range(100))
print(cnt)
b = time.time()
print(b-a)