import json
import os

class Dialogue:
    # 事件ID
    dialogue_id: int
    # 事件名称
    dialogue_name: str
    # 事件内容
    dialogue_list: list[dict] = []
    # "question": 说明, "options": 选项, "trigger":  触发效果[触发效果, 其他参数]
    # 触发效果: 1、增减最大生命值, 2、增减生命值, 3、获得遗物
    # 如果不同角色效果不同, [1] == None, 然后去索引[2]的字典

    # 事件类型 ： 1、Info信息展示,2、Choice事件选择,3、Confirm二次确认(高风险)||辅助类型4+
    dialogue_type: int = 0

    def __init__(self, dialogue_id: int):
        file_path = r'src\Game\map\al_dialogue.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.dialogue_id = dialogue_id
                self.dialogue_name = data[str(dialogue_id)]['dialogue_name']
                self.dialogue_list = data[str(dialogue_id)]['dialogue_list']
                self.dialogue_type = data[str(dialogue_id)]['dialogue_type']
        except Exception as e:
            print(f"读取文件时发生错误: {e}")

    from ..common import Room

    # 触发效果
    def trigger(self, list_ : list, room: 'Room'):
        if list_[0] == 1:
            room.player.max_HP += list_[1]
            room.player.HP += list_[1]
            room.player.HP = min(room.player.HP, room.player.max_HP)
            room.player.HP = max(room.player.HP, 1)
        elif list_[0] == 2:
            room.player.HP += list_[1]
            room.player.HP = min(room.player.HP, room.player.max_HP)
            room.player.HP = max(room.player.HP, 1)
        elif list_[0] == 3:
            from ..common import Relic
            room.player.relic.append(Relic(list_[1]))

    # 运行对话
    def run(self, room: Room):
        for log_dict in self.dialogue_list:
            print(log_dict['question'])
            for i in log_dict['options']:
                print(i)
            inp = 0
            while True:
                try:
                    os.system("cls")
                    inp = int(input("请输入选项: ").strip()) - 1
                except ValueError:
                    inp = -1
                if len(log_dict["trigger"]) == 1 or (inp >= 0 and inp < len(log_dict["trigger"])):
                    break
            self.trigger(log_dict['trigger'][str(inp)], room)
            os.system("cls")