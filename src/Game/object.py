import json
from .common import Buff
from .intent import Intent

class Object:
    """游戏对象类"""
    # 对象ID
    object_id: int = 0
    # 对象名称
    name: str = "无"
    # 生命值
    max_HP: int
    # 当前生命值
    HP: int = max_HP
    # 格挡
    block: int = 0
    # BUFF
    buff: list[Buff] = []
    # 第一个意图索引
    # [0]是None，则多种随机 or [0]是0，则根据某些值
    ## [0] == 0::
    # [1]如果是1，则根据位置设置初始意图，一个字典{0: 1}0的索引代表默认，其他索引是对应站位意图
    start_index: list = [0]
    # 意图
    intents: list[Intent] = []

    trigger_variables = [
        "max_HP",
        "block",
        "buff",
        "start_index"
    ]

    def __init__(self, object_id: int):
        file_path = r'src\Game\al_object.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            object_data = data[object_id]
            keys = object_data.keys()
            for key_ in keys:
                if key_ in self.trigger_variables:
                    setattr(self, key_, object_data[key_])
            
        except Exception as e:
            print(f"读取文件时发生错误: {e}")