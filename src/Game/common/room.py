from ..all_card_type import Card
from ..object import Object
from ..start_game import Game

# 玩家
class Player(Game):
    """玩家类"""
    # 当前出牌
    now_card: Card
    # 手牌
    hand_pile: list[Card]
    # 抽牌堆
    draw_pile: list[Card]
    # 弃牌堆
    discard_pile: list[Card]
    # 消耗牌堆
    exhaust_pile: list[Card]
    # 当前能量
    energy: int
    # 构建函数
    def __init__(self, game: Game):
        super().__init__(game.name, game.max_HP, game.HP, game.gold, game.relic)
        self.draw_pile = game.all_card
        self.energy = game.max_energy

class Room:
    """房间类"""
    player: Player
    # 玩家
    enemy: list[Object]
    # 敌人

    def __init__(self, player: Player, enemy: list[Object]):
        self.player = player
        self.enemy = enemy
