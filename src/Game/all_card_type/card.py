import json

# 卡牌
class Card:
    # 卡牌ID
    card_id: int
    # 名字
    name: str
    # 描述
    description: str
    # 消耗的能量，如果是X，此值为None
    spend_energy: int
    # 类型: 1 攻击， 2 技能， 3  能力， 4 状态/诅咒
    type: int
    # 是否消耗
    delete: bool = False
    # 是否可打出
    can_play: bool = True
    # 是否有特殊效果
    t_effect: bool = False
    # 特殊效果数据
    # 1 重复卡牌
    # # 额外判定数据: [
    # #     int = 1:buff[1: buff ID, 2: buff count]
    # #     
    # # ]
    t_effect_data: list = []
    # 效果
    effect_data: dict = {}
    # 攻击效果{
    #    # 是否AOE
    #    "is_aoe": False,
    #    # 伤害
    #    "damage": 0,
    #    # 触发次数
    #    "trigger_count": 0,
    #    # 是否格挡
    #    "is_block": True,
    #    # 格挡值
    #    "block": 0,
    #    # 是否有BUFF
    #    "is_buff": False,
    #     # 增益/减益
    #    "buff": [num, [int: ID, int: count],...],
    #    }

    # 技能效果{
    #    # 是否格挡
    #    "is_block": True,
    #    # 格挡值
    #    "block": 0,
    #    # 是否有BUFF
    #    "is_buff": False,
    #     # 增益/减益
    #    "buff": [num, [int: ID, int: count, me?],...],
    #    }

    trigger_variables = [
        "card_id",
        "name",
        "spend_energy",
        "type",
        "delete",
        "can_play",
        "effect_data"
    ]

    # 初始化
    def __init__(self, card_id: int):
        self.card_id = card_id
        file_path = r"src\Game\all_card_type\al_card.json"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            keys = data.keys()
            for key in keys:
                if key in self.trigger_variables:
                    setattr(self, key, data[key])
        except Exception as e:
            print(f"读取文件时发生错误: {e}")

    # 攻击牌使用,输出基础伤害
    def use_attack(self) -> int:
        base_damage = self.effect_data["damage"]
        return base_damage
    
    # 有格挡数值牌使用
    def use_block(self) -> int:
        base_block = self.effect_data["block"]
        return base_block
    
    # 弃牌
    def discard(self, hand_pile: list['Card'], discard_pile: list['Card']):
        if self in hand_pile:
            hand_pile.remove(self)
            discard_pile.append(self)
            return True
        else:
            print("卡牌无法弃牌")
        return False
    
    # 输出卡牌-模版
    def prt_card(self):
        msg = ""
        if self.spend_energy != None:
            msg = f"{self.spend_energy}-"
        else:
            msg = "X-"
        msg += f"{self.type}"


    # 输出牌组
    def prt_pile(self, pile: list['Card']):
        for card in pile:
            card.prt_card()