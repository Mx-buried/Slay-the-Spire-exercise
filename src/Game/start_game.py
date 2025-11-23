from .map import Map
from .map import Node
from .common import Buff, Relic
from .all_card_type import Card
from .object import Object

class Game:
    """游戏类"""
    name: str
    # 生命值
    max_HP: int
    HP: int
    # 护甲
    block: int
    # 金币
    gold: int
    # 遗物
    relic: list[Relic]
    # 节点
    now_node: Node
    #  buff
    buff: list[Buff]
    # 卡牌
    card: list[Card]
    # 地图
    map: Map
    # 卡牌背包
    all_card: list[Card] = []
    # 能量最大值&当前能量
    max_energy: int = 3

    def __init__(self, name: str, max_HP: int, gold: int, relic: list[int] = []):
        """创建游戏"""
        self.name = name
        self.max_HP = max_HP
        self.HP = max_HP
        self.gold = gold
        self.relic = [Relic(i) for i in relic]
        self.map = Map()
        self.now_node = self.map.map_all[0][0]
    
    def prt_Game(self):
        """输出信息"""
        msg = "玩家信息: \n"
        if self.block > 0:
            msg = f"\033[36m格挡:{self.block}\033[0m "
        msg += (
                f"\033[31mHP:{self.HP}/{self.max_HP}\033[0m " +
                f""
            )
        print(msg)

def new_game(name: str, max_HP: int, gold: int = 0, relic: list[int] = []) -> Game:
    """创建游戏"""
    GAME = Game(name, max_HP, gold, relic)
    return GAME