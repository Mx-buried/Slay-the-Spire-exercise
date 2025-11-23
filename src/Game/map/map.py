import random
import os
from .node import Node

class Map:
    # 地图
    map_all: list[list[Node]] = []
    # 本位面历史节点
    history_node: list[Node] = []
    # 地图长度
    map_length: int = 15
    # 当前位面
    now_plane: int = 0
    # 宽度概率
    Probability = [1,1,2,2,2,3,3,3,4,4,4]
    # 创建地图
    def map_create(self, map_length: int) -> list[list[Node]]:
        map_all = []
        for i in range(map_length):
            # boss
            if i == 0:
                map_all.insert(0, [Node(0, i)])
            # boos前休整
            elif i == 1:
                map_all.insert(0, [Node(2, i)])
            # 位面第一间小怪
            elif i == map_length - 1:
                map_all.insert(0, [Node(3, i)])
            else:
                # 宽度
                now_width = random.choice(self.Probability)
                # 如果为1,创建节点组 3 or 5 or 2
                if now_width == 1:
                    map_all.insert(0, [Node(random.choice([3, 5, 2]), i)])
                    continue
                # 节点类型,0-6 对应图标["💀","💰","🔥","👻","😈","💎","❓"]
                _Probability = [1,2,2,3,4,4,5,6]
                # 创建节点组
                temp_node = []
                for _ in range(now_width):
                    # 创建节点
                    temp = Node(random.choice(_Probability), i)
                    temp_node.append(temp)
                    # 添加概率3
                    if temp.type != 3 and 3 in _Probability:
                        _Probability.extend([3, 3])
                    # 删除概率3
                    else:
                        while 3 in _Probability:
                            _Probability.remove(3)
                    # 添加概率6
                    if temp.type != 6 and 6 in _Probability:
                        _Probability.extend([6, 6])
                    # 删除概率6
                    else:
                        while 6 in _Probability:
                            _Probability.remove(6)
                    # 删除当前概率
                    while temp.type in _Probability:
                        _Probability.remove(temp.type)
                temp_node.sort(key=lambda x: x.type)
                map_all.insert(0, temp_node)

        return map_all

    # 创建地图类
    def __init__(self):
        self.map_all.insert(0, [Node(6, 0)])

    # 位面++
    def plane_add(self):
        self.now_plane += 1
        os.system("cls")
        if self.now_plane < 4:
            a1 = ["???", "一", "二", "三"]
            a2 = ["???", "塔底", "城市", "深处"]
            msg = f"第{a1[self.now_plane]}阶段: "
            msg += a2[self.now_plane]
            print(msg)
            print()
            self.map_all = self.map_create(self.map_length)
            self.history_node = []
            self.print_map()
        elif self.now_plane == 4:
            msg = "第四阶段: 终幕"
            print(msg)
            print()
            self.map_length = 4
            self.map_all = []
            self.history_node = []
            self.map_all.insert(0, [Node(0, 0)])# 💀
            self.map_all.insert(0, [Node(4, 1)])# 😈
            self.map_all.insert(0, [Node(1, 2)])# 💰
            self.map_all.insert(0, [Node(2, 3)])# 🔥
            self.print_map()
        else:
            msg = "???????: ????"
            print(msg)
            print()
            self.map_length = 1
            self.map_all = []
            self.history_node = []
            self.map_all.insert(0, [Node(6, 0)])
            self.print_map()



    # 输出地图
    def print_map(self):
        for i in reversed(self.map_all):
            msg = "["
            for j in i:
                msg += j.get_icon()
                msg += " "
            print(msg + "]")
        for i in reversed(self.history_node):
            msg = "["
            msg += i.get_icon()
            msg += " "
            print(msg + "]")

    # 获取玩家选择节点 
    def select_node(self):
        inp = 0
        while True:
            try:
                os.system("cls")
                inp = int(input("请选择一个节点:(一个整数)").strip())
            except ValueError:
                inp = -1
            if len(self.map_all[0]) == 1 or (inp >= 0 and inp < len(self.map_all[0])):
                break
            os.system("cls")
        self.history_node.insert(0, self.map_all[0][inp])
        self.map_all.pop(0)
        from .node import enter_node
        enter_node(self.history_node[0], self.now_plane)