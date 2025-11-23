from ..start_game import Game
from .room import Room, Player
from ..object import Object

# 引入遗物
from .relic import Relic
from ..all_card_type import draw

# 开始战斗
def battleing(game: Game, enemy_: list[Object]):
    player = Player(game)
    enemy = enemy_
    Battle = Room(player, enemy)
    del(enemy)
    del(player)
    # 触发战斗开始效果
    battle_start_relics = [i for i in Battle.player.relic if i.on_battle_start]
    # 触发效果
    for relic in battle_start_relics:
        relic.trigger(Battle, "on_battle_start")
    # 战斗
    while Battle.player.HP > 0 and Battle.enemy != []:
        print("开始战斗,你的回合")
        draw(Battle.player.draw_pile, Battle.player.hand_pile, 5)
        # 触发回合开始遗物
        turn_start_relics = [i for i in Battle.player.relic if i.on_turn_start]
        for relic in turn_start_relics:
            relic.trigger(Battle, "on_turn_start")
