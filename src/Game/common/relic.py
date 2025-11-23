import json
import math

class Relic:
    """遗物类"""
    # 遗物ID
    relic_id: int = 0
    # 遗物名称
    name: str
    # 是否显示
    is_show: bool = True
    # 计数
    relic_count: int = 0
    # 触发时机:
    # [触发效果, 触发次数]# 规则：
    # 触发效果: 
    #   # 1: 摸牌， ::x:牌数
    #   # 2: 增减我方血量   ::1：百分数增减;;2：固定值::
    #   # 3：增减敌方血量
    #   # 4: 计数器触发 ::
    #   # 5: 更改某个值 ::
    #   # 99: 触发多次
    # # 战斗开始
    on_battle_start: bool = False
    # 战斗开始触发效果
    on_battle_start_effect: list = [0]
    # 战斗结束
    on_battle_end: bool = False
    # 战斗中:
    # 每一回合开始
    on_turn_start: bool = False
    # 牌使用
    on_card_play: bool = False 
    # 每一回合结束
    on_turn_end: bool = False 
    # 牌攻击触发
    on_attack: bool = False 
    # 牌格挡触发
    on_block: bool = False 
    # 对方攻击
    # 被伤害触发
    on_damage_taken: bool = False 
    # 被攻击触发
    on_attacked: bool = False 
    # 死亡？# 死亡触发
    on_death: bool = False
    # 计数满触发
    on_counter_full: bool = False
    # 计数器
    on_counter_full_count: list[int, int, int] = [999, 0, 0] # [计数器触发数, 计数器初始, 计数器+/-]
    # 计数器满触发
    on_counter_full_effect: list = [0]
    # 无条件触发
    NULL: bool = False
    # 无条件触发效果
    NULL_effect: list = [0]

    # 键名
    trigger_variables = [
    "on_battle_start",
    "on_battle_end",
    "on_turn_start",
    "on_card_play",
    "on_turn_end",
    "on_attack",
    "on_block",
    "on_damage_taken",
    "on_attacked",
    "on_death",
    "on_battle_start_effect",
    "on_battle_end_effect",
    "on_turn_start_effect",
    "on_card_play_effect",
    "on_turn_end_effect",
    "on_attack_effect",
    "on_block_effect",
    "on_damage_taken_effect",
    "on_attacked_effect",
    "on_death_effect",
    "on_counter_full",
    "on_counter_full_count",
    "on_counter_full_effect"
]
    def __init__(self, number_: int):
        number = str(number_)
        file_path = r'src/Game/common/al_relic.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            if number in data:
                relic_data = data[number]
                data_key = relic_data.keys()
                self.name = relic_data['name']
                self.relic_id = number_
                # 遗物处理
                for i in data_key:
                    if i in self.trigger_variables:
                        setattr(self, i, relic_data[i])
                    if i == "on_counter_full_count":
                        self.relic_count = relic_data[1]
            
        except Exception as e:
            print(f"读取文件时发生错误: {e}")


    from .battle_time import Room
    def trigger(self, room: 'Room', trigger_type: str) -> int:
        from ..all_card_type import draw, Card
        from .battle_time import Room
        effect_type = trigger_type + "_effect"
        # 触发效果
        if getattr(self, trigger_type):
            # 效果1：抽牌
            if getattr(self, effect_type)[0] == 1:
                draw(room, getattr(self, effect_type)[1])
            # 效果2：增减玩家生命
            elif getattr(self, effect_type)[0] == 2:
                if getattr(self, effect_type)[1] == 1:
                    room.player.HP *= 1 + getattr(self, effect_type)[2]
                    room.player.HP = max(room.player.HP, 1)
                    room.player.HP = max(room.player.max_HP, room.player.HP)
                elif getattr(self, effect_type)[1] == 2:
                    room.player.HP += getattr(self, effect_type)[2]
                    room.player.HP = max(room.player.HP, 1)
                    room.player.HP = min(room.player.HP, room.player.max_HP)
            # 效果3: 增减敌方生命
            elif getattr(self, effect_type)[0] == 3:
                for enemy_ in Room.enemy:
                    if getattr(self, effect_type)[1] == 1:
                        enemy_.HP *= 1 + getattr(self, effect_type)[2]
                        enemy_.HP = max(enemy_.HP, 1)
                        enemy_.HP = min(enemy_.HP, enemy_.max_HP)
                    elif getattr(self, effect_type)[1] == 2:
                        enemy_.HP += getattr(self, effect_type)[2]
                        enemy_.HP = max(enemy_.HP, 1)
                        enemy_.HP = min(enemy_.HP, enemy_.max_HP)
            # 效果4: 计数器增减触发
            elif getattr(self, effect_type)[0] == 4:
                self.relic_count += getattr(self, trigger_type + "_count")[2]
                if self.relic_count >= getattr(self, trigger_type + "_count")[0]:
                    self.relic_count = getattr(self, trigger_type + "_count")[1]
                    self.trigger(room, "on_counter_full")
            # 效果5: 更改自身某值
            elif getattr(self, effect_type)[0] == 5:
                key_data = getattr(self, effect_type)[1].keys()
                for key in key_data:
                    setattr(self, key, getattr(self, effect_type)[1][key])
            # 触发多种效果
            elif getattr(self, effect_type)[0] == 99:
                for trigger_temp in getattr(self, effect_type)[1]:
                    temp_relic = Relic(0)
                    temp_relic.is_show = False
                    setattr(temp_relic, "NULL", True)
                    setattr(temp_relic, "NULL_effect", trigger_temp)
                    temp_relic.trigger(room, "NULL")
                    del(temp_relic)
