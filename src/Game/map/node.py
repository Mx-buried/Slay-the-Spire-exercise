class Node:
    # 节点类型,0-6 对应图标["💀","💰","🔥","👻","😈","💎","❓"]
    type: int
    # 距离boss的距离
    now_node: int
    # 节点图标
    icon: list[str] = ["💀", "💰", "🔥", "👻", "😈", "💎", "❓"]

    # 节点初始化
    def __init__(self, type: int, now_node: int):
        self.type = type
        self.now_node = now_node

    def get_icon(self) -> str:
        return self.icon[self.type]

def enter_node(now_node:list[Node, int]):
    self_ = now_node[0]
    # boss节点
    if self_.type == 0:
        1
    # 商店节点
    elif self_.type == 1:
        1
    # 休整节点
    elif self_.type == 2:
        1
    # 小怪节点
    elif self_.type == 3:
        1
    # 精英节点
    elif self_.type == 4:
        1
    # 宝箱节点
    elif self_.type == 5:
        1
    # 未知节点
    elif self_.type == 6:
        if now_node[1] == 0:
            run_dialogue(1)

def run_dialogue(number_: int):
    from .dialogue import Dialogue
    now_dialogue = Dialogue(number_)
    now_dialogue.run()
