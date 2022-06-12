import numpy
import random
from ...base.player import Player
import json

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)

    def reset(self):
        super().reset()
        self.__history = []
        self.__mode = 1
        try:
            with open('gym_splendor/envs/agents/agent_Ann/Data/simple_greedy.json', 'r') as f:
                self.__data = numpy.array(json.load(f))
                
        except:
            self.__data = numpy.array([
                [1 for i in range(self.amount_action)],
                [1 for i in range(self.amount_action)]
            ])
            with open('gym_splendor/envs/agents/agent_Ann/Data/simple_greedy.json', 'w') as f:
                    f.write(
                        '[' + 
                        ',\n'.join(json.dumps([int(i) for i in ii]) for ii in self.__data)
                        + ']'
                    )

        self.__rating = self.__data[1] / self.__data[0]

    def action(self, dict_input):
        state = self.get_list_state(dict_input)
        v_ = self.check_victory(state)
        if v_ == -1:
            list_index_action = self.get_list_index_action(state)
            list_max_rating = numpy.where(self.__rating[list_index_action] == max(self.__rating[list_index_action]))[0]
            if self.__mode == 1 or numpy.random.uniform() <= 0.8:
                act_ = random.choice(list_max_rating)
                action = list_index_action[act_]
            else:
                try:
                    act_ = random.choice([i for i in range(list_index_action.__len__()) if i not in list(list_max_rating)])
                except:
                    act_ = random.choice(list_max_rating)

                action = list_index_action[act_]

            self.__history.append(action)
            return action
        
        else:
            if self.__mode == 0:
                with open('gym_splendor/envs/agents/agent_Ann/Data/simple_greedy.json', 'r') as f:
                    data = numpy.array(json.load(f))

                if v_ == 1:
                    for action in self.__history:
                        data[:,action] += [1,1]

                else:
                    for action in self.__history:
                        data[:,action] += [1,0]

                with open('gym_splendor/envs/agents/agent_Ann/Data/simple_greedy.json', 'w') as f:
                    f.write(
                        '[' + 
                        ',\n'.join(json.dumps([int(i) for i in ii]) for ii in data)
                        + ']'
                    )
            else:
                pass