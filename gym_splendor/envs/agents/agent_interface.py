from gym_splendor.envs.agents.agent_Ann import agent_Ann as p1
# from gym_splendor.envs.agents.agent_Ann import agent_Ann as p2
# from gym_splendor.envs.agents.agent_Ann import agent_Ann as p3
# from gym_splendor.envs.agents.agent_Ann import agent_Ann as p4


# from gym_splendor.envs.agents.agent_A import agent_A as p1
from gym_splendor.envs.agents.agent_A import agent_A as p2
from gym_splendor.envs.agents.agent_A import agent_A as p3
from gym_splendor.envs.agents.agent_A import agent_A as p4

lst = [p1, p2, p3, p4]
lst_name = ['Annnnnnnnn', 'BOT2', 'BOT3', 'BOT4']

list_players = [lst[i].Agent(lst_name[i]) for i in range(lst.__len__())]