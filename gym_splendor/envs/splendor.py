import gym
import random
import numpy
import json
from colorama import Fore, Style
from gym_splendor.envs.base.board import Board
from gym_splendor.envs.agents import agent_interface

class splendorEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        with open('gym_splendor/envs/action_space.json') as f:
            self.full_action = json.load(f)

        self.board = Board()
        self.turn = None
        self.amount_player = None
        self.players = None
        self.dict_input = None

    def reset(self):
        self.board.reset()
        self.turn = 0
        self.amount_player = min(agent_interface.list_players.__len__(), 4)
        self.adjust_starting_stocks(self.amount_player)
        self.players = random.sample(agent_interface.list_players, k=self.amount_player)
        for p in self.players:
            p.reset()

        self.dict_input = {
            'Turn': self.turn,
            'Board': self.board,
            'Players': [self.players[(self.turn+1+i)%self.amount_player] for i in range(self.amount_player-1)],
            'End_game': False,
        }

    def render(self, mode='human', close=False):
        print('----------------------------------------------------------------------------------------------------')
        print('Turn:', self.turn, 'Board stocks:', self.board.stocks)
        for k in [3,4,5]:
            print(f'card level {k-2}:', self.board.normal_cards[k], end=' ')
            pass
        
        print('card noble:', self.board.noble_cards)
        for p in self.players:
            print(p.name, p.score, p.stocks, p.stocks_const, p.opened_cards, p.upside_cards)
            pass

    def close(self):
        if (self.turn+1) % self.amount_player == 0 and self.board.current_highest_score >= 15:
            self.dict_input['End_game'] = True
            return True

        self.turn += 1
        self.dict_input['Turn'] = self.turn
        self.dict_input['Players'] = [self.players[(self.turn+1+i)%self.amount_player] for i in range(self.amount_player-1)]
        return False

    def step(self, action_player):
        current_player = self.players[self.turn % self.amount_player]
        try:
            action = self.full_action[action_player]
        except:
            action = action_player.copy()

        if action[0] == 1: # L???y nguy??n li???u
            if self.check_get_stocks(current_player, numpy.array(action[1]), numpy.array(action[2])):
                self.get_stocks(current_player, numpy.array(action[1]), numpy.array(action[2]))
                
        elif action[0] == 2: # L???y th???
            if self.check_get_card(current_player, action[1]):
                self.get_card(current_player, action[1])
                
        elif action[0] == 3: # ??p th???
            if self.check_upside_card(current_player, action[1], numpy.array(action[2])):
                self.upside_card(current_player, action[1], numpy.array(action[2]))

        else:
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: tham s??? ch??? ?????nh h??nh ?????ng kh??ng ????ng', Style.RESET_ALL)
            input()
            pass

        return None, None, self.close(), None

    # ****************************************************************************************************

    def upside_card(self, current_player, card_id, stocks_return):
        # Nh???n nguy??n li???u v??ng
        if self.board.stocks[5] > 0:
            current_player._Player__stocks[5] += 1
            self.board._Board__stocks[5] -= 1

        # Tr??? nguy??n li???u n???u th???a
        if sum(current_player.stocks) > 10:
            current_player._Player__stocks -= stocks_return
            self.board._Board__stocks += stocks_return

        # Th??m v??o ch???ng th??? ??p
        if card_id in [100,200,300]:
            current_player._Player__upside_cards.append(self.board._Board__normal_cards[int(card_id/100)-1].pop())
            # print(Fore.LIGHTGREEN_EX, current_player.name, f'??p th??? ???n c???p {int(card_id/100)}', Style.RESET_ALL)

        else:
            for k in [3,4,5]:
                if card_id in self.board.normal_cards[k]:
                    current_player._Player__upside_cards.append(card_id)
                    self.board._Board__normal_cards[k].remove(card_id)
                    # print(Fore.LIGHTGREEN_EX, current_player.name, '??p th???', card_id, Style.RESET_ALL)
                    try:
                        self.board._Board__normal_cards[k].append(self.board._Board__normal_cards[k-3].pop())
                    except:
                        pass

                    break

    def check_upside_card(self, current_player, card_id, stocks_return):
        if current_player.upside_cards.__len__() == 3:
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: kh??ng th??? ??p th??m th??? n???a do ???? c?? 3 th??? ??ang ??p', Style.RESET_ALL)
            input()
            return False

        if card_id in [100,200,300]:
            if self.board.normal_cards[int(card_id/100)-1].__len__() == 0:
                # print(Fore.LIGHTRED_EX, current_player.name, f'l???i kh??ng c??n th??? ???n c???p {int(card_id/100)} ????? m?? ??p', Style.RESET_ALL)
                input()
                return False

        else:
            if card_id not in (self.board.normal_cards[3] + self.board.normal_cards[4] + self.board.normal_cards[5]):
                # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: ??p th??? kh??ng xu???t hi???n tr??n b??n ch??i', Style.RESET_ALL)
                input()
                return False

        pl_st_after = current_player.stocks.copy()
        if self.board.stocks[5] > 0:
            pl_st_after[5] += 1

        if sum(pl_st_after) > 10:    
            pl_st_after -= stocks_return

        if (pl_st_after < 0).any() or sum(pl_st_after) > 10:
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: tr??? ch??a ????? nguy??n li???u ho???c tr??? nguy??n li???u kh??ng c??', Style.RESET_ALL)
            input()
            return False

        return True

    def get_card(self, current_player, card_id):
        # Tr??? nguy??n li???u
        player_stocks = current_player.stocks[:5]
        card_infor = self.board.cards_infor[card_id]
        card_price = card_infor[-5:]
        nl_bo_ra = (card_price > current_player.stocks_const) * (card_price - current_player.stocks_const)
        nl_bt = numpy.minimum(nl_bo_ra, player_stocks)
        nl_auto = sum(nl_bo_ra - nl_bt)

        current_player._Player__stocks[:5] -= nl_bt
        current_player._Player__stocks[5] -= nl_auto
        self.board._Board__stocks[:5] += nl_bt
        self.board._Board__stocks[5] += nl_auto
        # print(Fore.LIGHTGREEN_EX, current_player.name, 'l???y th???:', card_id, 'tr??? nguy??n li???u th?????ng:', nl_bt, 'nguy??n li???u auto:', nl_auto, Style.RESET_ALL)

        # Nh???n th???
        try:
            current_player._Player__upside_cards.remove(card_id)
        except:
            for k in [3,4,5]:
                if card_id in self.board.normal_cards[k]:
                    self.board._Board__normal_cards[k].remove(card_id)
                    try:
                        self.board._Board__normal_cards[k].append(self.board._Board__normal_cards[k-3].pop())
                    except:
                        pass

                    break

        current_player._Player__opened_cards.append(card_id)

        # Stock const, score
        current_player._Player__stocks_const[card_infor[1]] += 1
        current_player._Player__score += card_infor[0]

        # Check th??? Noble
        noble_lst = []
        for noble_id in self.board.noble_cards:
            if(self.board.cards_infor[noble_id][-5:] <= current_player.stocks_const).all():
                noble_lst.append(noble_id)
        
        for noble_id in noble_lst:
            self.board._Board__noble_cards.remove(noble_id)
            current_player._Player__opened_cards.append(noble_id)
            current_player._Player__score += 3
            # print(Fore.LIGHTGREEN_EX, current_player.name, 'nh???n th??? Noble', noble_id, Style.RESET_ALL)
        
        if current_player.score > self.board.current_highest_score:
            self.board._Board__current_highest_score = current_player.score
        
    def check_get_card(self, current_player, card_id):
        if card_id not in (current_player.upside_cards + self.board.normal_cards[3]
                            + self.board.normal_cards[4] + self.board.normal_cards[5]):
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: mua th??? kh??ng xu???t hi???n tr??n b??n ch??i ho???c ch???ng th??? ??p', Style.RESET_ALL)
            input()
            return False

        player_stocks = current_player.stocks[:5] + current_player.stocks_const
        card_price = self.board.cards_infor[card_id][-5:]
        if sum((card_price > player_stocks) * (card_price - player_stocks)) <= current_player.stocks[5]: # ????? nguy??n li???u l???y th???
            return True

        # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: kh??ng ????? nguy??n li???u l???y th???', Style.RESET_ALL)
        input()
        return False

    def get_stocks(self, current_player, stocks, stocks_return):
        # L???y nguy??n li???u
        current_player._Player__stocks[:5] += stocks
        self.board._Board__stocks[:5] -= stocks
        # print(Fore.LIGHTGREEN_EX, current_player.name, 'l???y nguy??n li???u:', stocks, end='')

        # Tr??? nguy??n li???u
        if sum(current_player.stocks) > 10:
            current_player._Player__stocks -= stocks_return
            self.board._Board__stocks += stocks_return
            # print(' tr??? nguy??n li???u:', stocks_return, end='')
        
        # print(Style.RESET_ALL)

    def check_get_stocks(self, current_player, stocks, stocks_return):
        _sum_stocks = sum(stocks)
        if _sum_stocks > 3:
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: l???y qu?? 3 nguy??n li???u', Style.RESET_ALL)
            input()
            return False
        
        if _sum_stocks == 3 and (stocks > 1).any():
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: l???y 3 nguy??n li???u tuy nhi??n c?? ??t nh???t 2 nguy??n li???u c??ng m??u', Style.RESET_ALL)
            input()
            return False

        if _sum_stocks == 2 and (stocks == 2).any() and self.board.stocks[numpy.where(stocks==2)[0][0]] < 4:
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: l???y 2 nguy??n li???u c??ng m??u tuy nhi??n kh??ng ????? ??i???u ki???n tr??n b??n ch??i', Style.RESET_ALL)
            input()
            return False
        
        if ((self.board.stocks[:5] - stocks) < 0).any():
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: l???y nguy??n li???u m?? b??n ch??i kh??ng c??', Style.RESET_ALL)
            input()
            return False

        pl_st_after = current_player.stocks.copy()
        pl_st_after[:5] += stocks
        if sum(pl_st_after) > 10:
            pl_st_after[:6] -= stocks_return

        if sum(pl_st_after) > 10 or (pl_st_after < 0).any():
            # print(Fore.LIGHTRED_EX, current_player.name, 'l???i: tr??? ch??a ????? nguy??n li???u ho???c tr??? nguy??n li???u kh??ng c??', Style.RESET_ALL)
            input()
            return False
        
        return True

    def adjust_starting_stocks(self, amount_player):
        if amount_player not in [1,4]:
            self.board._Board__stocks -= numpy.array([1,1,1,1,1,0]) * (4-amount_player) + numpy.array([1,1,1,1,1,0])