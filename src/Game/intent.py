import json

class Intent:
    # 意图来源ID
    source_id: int = 0
    # 意图ID
    intent_id: int = 0
    # 意图：1 攻击 2 回血回盾 3 buff
    intent_type: int = 0
    # 参数
    # 1.[数值，次数]
    # 2.[数值]
    # 3.[buff个数, [[buff_id, buff_count], ...]]
    parameter: list = [0]
    # 是否对我方释放
    is_me: bool = False
    # 是否对群释放
    is_all: bool = False
    # 下一个技能索引 如果是随机组，则-4为None在-5随机 -4
    next_intent: int = 0
    # 技能池
    intent_pool: list[int] = []

    trigger_variables = [
        "intent_type",
        "parameter",
        "is_me",
        "is_all",
        "next_intent",
        "intent_pool"
    ]

    def __init__(self,source_id: int, intent_id: int):
        self.source_id = source_id
        self.intent_id = intent_id
        file_path = r"src\Game\al_object.json"
        try: 
            with open(file_path, 'r', encoding='utf-8') as f: 
                data = json.load(f)
            intent_data = data[str(source_id)]["intent"][str(intent_id)]
            intent_data_key = intent_data.keys()
            for i in intent_data_key: 
                if i in self.trigger_variables: 
                    setattr(self, i, intent_data[i])

        except Exception as e: 
            print(f"读取文件时发生错误: {e}")