import math

class Buff:
    # buffID
    buff_id: int
    # buff当前对象
    object_: list = [True, 0] # [bool: 是否为Player, object_id:]
    # buff计数
    buff_count: int = 0
    # 每回合是否掉buff_count
    is_drop_buff_count: bool = False
    # 掉多少
    drop_buff_count: int = 0
    # 是否会变成负数
    negative: bool = False
    # 触发
    # 无条件触发
    NULL: bool = False
    NULL_effect: list = [0]
    # 每一回合开始
    on_turn_start: bool = False
    on_turn_start_effect: list = [0, 0]
    # 牌使用
    on_card_play: bool = False
    card_type: int = 0 # 牌类型
    on_card_play_effect: list = [0] # 触发效果: [卡牌种类]
    # 每一回合结束
    on_turn_end: bool = False
    on_turn_end_effect: list = [0, 0]
    # 被伤害
    on_damage_taken: bool = False
    on_damage_taken_effect: list = [0, 0]
    # 被攻击
    on_attacked: bool = False
    on_attacked_effect: list = [0, 0] # 触发效果: [效果类型: 1、增减伤害数值;2、百分比增减, 触发效果参数]
    # 攻击时
    on_attack: bool = False
    on_attack_effect: list = [0, 0] # 触发效果: [效果类型：1、增减伤害数值;2、百分比增减, 触发效果参数]
    # 格挡时
    on_block: bool = False
    on_block_effect: list = [0, 0]
    # 死亡时
    on_death: bool = False
    on_death_effect: list = [0]
    # 键名
    trigger_variables = [
        "buff_count",
        "drop_buff_count",
        "negative",
        "card_type",
        "on_turn_start",
        "on_card_play",
        "on_turn_end",
        "on_damage_taken",
        "on_attacked",
        "on_attack",
        "on_block",
        "on_death",
        "on_turn_start_effect",
        "on_card_play_effect",
        "on_turn_end_effect",
        "on_damage_take_effect",
        "on_attacked_effect",
        "on_attack_effect",
        "on_block_effect",
        "on_death_effect",
        ]
    # effect：
    # 1. 增减血量 :: [效果类型, 1、百分比增减, 触发效果参数;2、增减伤害数值]
    # 2. 增减格挡 :: [效果类型, 1、百分比增减, 触发效果参数;2、增减数值]
    # 3. 增减能量 :: [效果类型, 增加的数值]
    # 5. 增减buff :: [效果类型, buffID, 增减的数值: None代表当前buff数值, 是否我方, 是否对群]
    # 99.触发多次 :: [99, [效果类型, 触发效果参数], ...]

    def __init__(self, number_: int, object_: list, buff_count: int):
        import json
        number = str(number_)
        file_path = r'src/Game/common/al_buff.json'
        try:
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            # 检查键名
            if number in data:
                buff_data = data[number]
                data_key = buff_data.keys()
                self.name = buff_data['name']
                self.buff_id = number_
                # buff处理
                for i in data_key:
                    if i in self.trigger_variables:
                        setattr(self, i, buff_data[i])
        
        except Exception as e:
            print(f"读取文件时发生错误: {e}")

    from .room import Room
    # 非攻击触发
    def trigger(self, room: 'Room', trigger_type: str):
        from .battle_time import Room
        from ..object import Object
        from ..start_game import Game
        effect_type = trigger_type + "_effect"
        # 如果是牌触发验证一下类型
        if trigger_type == "on_card_play" and self.card_type != room.player.now_card.type:
            return
        if getattr(self, trigger_type):
            # 血量
            if getattr(self, effect_type) == 1:
                if self.object_[0]:
                    obj = room.player
                else:
                    obj = room.enemy[self.object_[1]]
                # 触发效果
                if getattr(self, effect_type)[1] == 1:
                    obj.HP *= 1 + getattr(self, effect_type)[2]
                    obj.HP = max(obj.HP, 1)
                    obj.HP = min(obj.max_HP, obj.HP)
                elif getattr(self, effect_type)[1] == 2:
                    obj.HP += getattr(self, effect_type)[2]
                    obj.HP = max(obj.HP, 1)
                    obj.HP = min(obj.HP, obj.max_HP)
            # 护盾
            elif getattr(self, effect_type) == 2:
                if self.object_[0]:
                    obj = room.player
                else:
                    obj = room.enemy[self.object_[1]]
                # 触发效果
                if getattr(self, effect_type)[1] == 1:
                    obj.block *= 1 + getattr(self, effect_type)[2]
                    obj.block = max(obj.block, 0)
                    obj.block = min(obj.block, obj.max_block)
                elif getattr(self, effect_type)[1] == 2:
                    obj.block += getattr(self, effect_type)[2]
                    obj.block = max(obj.block, 0)
                    obj.block = min(obj.block, obj.max_block)
            # 能量
            elif getattr(self, effect_type) == 3:
                room.player.energy += getattr(self, effect_type)[1]
            # buff
            elif getattr(self, effect_type) == 5:
                buff_data = getattr(self, effect_type)
                buff_id = buff_data[1]
                buff_count_: int = getattr(self, effect_type)[2]
                object_ = []
                if buff_count_ == None:
                    buff_count_ = self.buff_count
                if buff_data[3]:
                    object_[0] = self.object_[0]
                else:
                    object_[0] = not self.object_[0]
                if not buff_data[4] or object_[0]:
                    object_[1] = 0
                    room.player.buff.append(Buff(buff_id, object_, buff_count_))
                else:
                    for enemy_ in room.enemy:
                        object_[1] = enemy_.object_id
                        enemy_.buff.append(Buff(buff_id, object_, buff_count_))



## 攻击时触发
#def trigger_attack(buffs: list[Buff], base_damage: int) -> int:
#    damage = base_damage
#    # 分类攻击效果
#    attack_effect_type_1_buffs = [
#        buff for buff in buffs
#        if buff.on_attack_effect[0] == 1
#    ]
#    attack_effect_type_2_buffs = [
#        buff for buff in buffs
#        if buff.on_attack_effect[0] == 2
#    ]
#    # 触发效果
#    for buff_ in attack_effect_type_1_buffs:
#        if buff_.on_attack_effect[1] != None:
#            damage += buff_.on_attack_effect[1]
#        else:
#            damage += buff_.duration
#    for buff_ in attack_effect_type_2_buffs:
#        damage *= 1 + buff_.on_attack_effect[1]
#        math.floor(damage)
#    return damage

# 攻击触发
def trigger_damage(buffs: list[Buff], base_damage: int, trigger_type: str) -> int:
    # 攻击效果
    damage = base_damage
    # 攻击效果分类类型
    effect_type = "on_" + trigger_type + "_effect"
    attar_type_1_buffs = [
        buff for buff in buffs
        if getattr(buff, effect_type)[0] == 1
    ]
    attar_type_2_buffs = [
        buff for buff in buffs
        if getattr(buff, effect_type)[0] == 2
    ]
    # 攻击效果
    for buff_ in attar_type_1_buffs:
        damage += getattr(buff_, effect_type)[1]
    for buff_ in attar_type_2_buffs:
        damage *= 1 + getattr(buff_, effect_type)[1]
        damage = math.floor(damage)
    # 触发效果
    return damage

def trigger_block(buffs: list[Buff], base_block: int) -> int:
    block = base_block
    block_effect_type_1_buffs = [
        buff for buff in buffs
        if buff.on_block_effect[0] == 1
    ]
    block_effect_type_2_buffs = [
        buff for buff in buffs
        if buff.on_block_effect[0] == 2
    ]
    for buff_ in block_effect_type_1_buffs:
        block += buff_.on_block_effect[1]
    for buff_ in block_effect_type_2_buffs:
        block *= 1 + buff_.on_block_effect[1]
        block = math.floor(block)

    return block
