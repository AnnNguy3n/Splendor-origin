import pandas
import random
import numpy

class Board:
    def __init__(self):
        self.name = 'Splendor: Board'
        self.__cards_infor = []

        # Đọc thẻ thường: 0 -> 89
        data = pandas.read_csv('gym_splendor/envs/base/cards_information/normal_cards.csv')
        for i in range(data.__len__()):
            temp = data.loc[i]
            self.__cards_infor.append(
                numpy.array(
                    [
                        int(temp['score']), # score
                        ['red', 'blue', 'green', 'black', 'white'].index(temp['type of stock']) # type stock
                    ] + [int(a) for a in temp['price'].split(', ')] # 'red', 'blue', 'green', 'black', 'white'
                )
            )

        # Đọc thẻ Noble: 90 -> 99
        data = pandas.read_csv('gym_splendor/envs/base/cards_information/noble_cards.csv')
        for i in range(data.__len__()):
            temp = data.loc[i]
            self.__cards_infor.append(
                numpy.array(
                    [
                        (int(temp['score'])), # score
                    ] + [int(a) for a in temp['price'].split(', ')] # 'red', 'blue', 'green', 'black', 'white'
                )
            )

        self.__stocks = None
        self.__normal_cards = None
        self.__noble_cards = None
        self.__current_highest_score = None

    def reset(self):
        # Stocks
        self.__stocks = numpy.array(
            [
                7, # red
                7, # blue
                7, # green
                7, # black
                7, # white
                5, # auto-color (gray)
            ]
        )

        # Normal cards
        self.__normal_cards = [
            [i for i in range(0, 40)], # thẻ cấp 1 chưa xuất hiện
            [i for i in range(40, 70)], # thẻ cấp 2 chưa xuất hiện
            [i for i in range(70, 90)], # thẻ cấp 3 chưa xuất hiện
            [], # thẻ cấp 1 hiện tại trên bàn chơi
            [], # thẻ cấp 2 hiện tại trên bàn chơi
            [], # thẻ cấp 3 hiện tại trên bàn chơi
        ]

        for i in range(3):
            random.shuffle(self.__normal_cards[i])
            for j in range(4):
                self.__normal_cards[i+3].append(self.__normal_cards[i].pop())

        # noble cards
        self.__noble_cards = random.sample([90+i for i in range(10)], k=5)

        # self.__current_highest_score
        self.__current_highest_score = 0

    @property
    def cards_infor(self):
        return self.__cards_infor.copy()

    @property
    def stocks(self):
        return self.__stocks.copy()

    @property
    def normal_cards(self):
        return self.__normal_cards.copy()

    @property
    def noble_cards(self):
        return self.__noble_cards.copy()

    @property
    def current_highest_score(self):
        return self.__current_highest_score