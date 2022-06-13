from gym_splendor.envs.base.player import Player
import random

class Agent(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def reset(self):
        super().reset()

    def action(self, dict_input):
        state = self.get_list_state(dict_input)
        list_index_action = self.get_list_index_action(state)
        action = random.choice(list_index_action)
        return action