from ..all_card_type import Card
from ..start_game import Game
from ..common import trigger_damage, trigger_block
from ..common import Room
import random

# 使用卡牌
def use(card: Card, room: Room):
    # 检索卡牌
    if card.can_play and card in room.player.hand_pile:
        # 临时存储
        room.player.now_card = card
        # 检索buff
        buffs_on_card_play = [buff for buff in room.player.buff if buff.on_card_play == True]
        for enemy_ in room.enemy:
            buffs_on_card_play.extend([buff for buff in enemy_.buff if buff.on_card_play == True])
        for buff in buffs_on_card_play:
            if buff.card_type == card.type:
                buff.trigger(room, "on_card_play")
        # 移除手牌
        room.player.hand_pile.remove(card)
        card.trigger
        if card.delete:
            room.player.exhaust_pile.append(card)
        else:
            room.player.discard_pile.append(card)
        room.player.now_card = None
        return True
    else:
        print("卡牌无法使用")
    return False

# 触发效果-模版
def trigger(card: Card, room: Room, object_: int):
    # 类型: 1 攻击， 2 技能， 3  能力， 4 状态/诅咒
    # 触发攻击牌
    if card.type == 1:
        damage = card.use_attack()
        # 检索伤害增减buff
        buffs_on_attack = [buff for buff in room.player.buff if buff.on_attack == True]
        # 触发效果
        damage = trigger_damage(buffs_on_attack, damage)
        # 删除变量
        del(buffs_on_attack)
        # 攻击
        if card.effect_data["is_aoe"]:
            for enemy_ in room.enemy:
                buffs_on_attack = [buff for buff in enemy_.buff if buff.on_attacked == True]
                temp_damage = trigger_damage(buffs_on_attack, damage)
                enemy_.HP -= temp_damage
                enemy_.HP = max(0, enemy_.HP)
            for enemy_ in room.enemy:
                if enemy_.HP <= 0:
                    buffs_on_death = [buff for buff in enemy_.buff if buff.on_death == True]
                    for buff in buffs_on_death:
                        buff.trigger(room, "on_death")
                    if enemy_.HP <= 0:
                        room.enemy.remove(enemy_)
        else:
            enemy_ = room.enemy[object_]
    elif card.type == 2:
        1
    if card.effect_data["is_block"]:
        block_num = card.use_block()
        buffs_on_block = [buff for buff in room.player.buff if buff.on_block == True]
        block_num = trigger_block(buffs_on_block, block_num)
        room.player.block += block_num
        room.player.block = max(0, room.player.block)
        del(buffs_on_block)
    if card.t_effect:
        if card.t_effect_data[0] == 1:
            temp_card = card
            temp_card.t_effect = False
            trigger(temp_card, room)




# 洗牌
def shuffle(room: Room):
    if Room.player.draw_pile == []:
        Room.player.draw_pile = Room.player.discard_pile
        Room.player.discard_pile = []

# 抽牌
def draw(room: Room, num: int):
    while num > 0:
        if len(room.player.draw_pile) > 0:
            room.player.hand_pile.append(random.choice(room.player.draw_pile))
            room.player.draw_pile.remove(room.player.hand_pile[-1])
            num -= 1
        elif room.player.discard_pile != []:
            shuffle(room)
        else:
            return False
    return True