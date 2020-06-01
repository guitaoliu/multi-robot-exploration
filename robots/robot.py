import numpy as np
from typing import Union

from robots.setting import (
    BOT_COMMUNICATE_RANGE,
    BOT_MOVING_RANGE,
    PROFIT_RATIO,
    PHE_RATIO,
)

from robots.maps import ExploreMap, PheMap, Node


class Robot:
    comm_range = BOT_COMMUNICATE_RANGE

    def __init__(self, node: Union[Node, tuple]):
        if isinstance(node, Node):
            self.node = node
        elif isinstance(node, tuple):
            self.node = Node(node)
        else:
            raise TypeError
        self.mov_range = BOT_MOVING_RANGE
        self.loc_barrier_map = ExploreMap()
        self.loc_explore_map = ExploreMap()
        self.moving_path = []
        self.explore_node_list = []

    def loc(self) -> tuple:
        return self.node.loc()

    def moving_profit(self, node: Node) -> Union[float, None]:
        if self.get_accessibility(node):
            moving_cost = self.get_manha_distance(node)
            phe = self.get_phe_level(node)
            explore_profit = self.get_explore_profit()
            r = np.exp(
                PROFIT_RATIO * explore_profit + (1 - PROFIT_RATIO) * (
                    moving_cost + PHE_RATIO * phe
                )
            )
            return r
        else:
            return None

    def get_manha_distance(self, node: Node) -> int:
        return np.abs(self.node.x - node.x) + np.abs(self.node.y - node.y)

    def get_accessibility(self, rob:Robot) -> bool:
        if np.sqrt((self.node.x - rob.node.x) ** 2 + (self.node.y - rob.node.y) ** 2) < Robot.comm_range:
            return True
        else:
            return False


    def get_phe_level(self, node: Node) -> float:
        phe_map = self.get_global_phe_map()
        return phe_map.get_phe(self.node, node)

    def get_global_phe_map(self) -> PheMap:
        # todo global phemap
        b = PheMap()
        return b

    def is_finished(self):
        return self.loc_explore_map.is_finished()

    def get_await_nodes(self) -> Node:
        pass

    def release_node_and_wait_for_buyer(self, botlist, target:Node) -> Robot:
        """botlist为空闲状态机器人队列"""
        maxval=self.get_explore_profit(target)
        res=self
        for bot in roblist:
            if self.get_accessibility(bot)==1:
                if bot.get_explore_profit(target)>maxval:
                    res=bot
        
        return res

                

    def explore(self):
        (x,y)=self.loc()
        for i in range(-BOT_MOVING_RANGE,BOT_MOVING_RANGE):
            for j in range(-BOT_MOVING_RANGE,BOT_MOVING_RANGE):
                if abs(i)+abs(j)<=BOT_MOVING_RANGE:
                    self.loc_explore_map.update(Node((x+i,y+j)))

    def get_explore_profit(self, target:Node) ->float:
        #D*算法，计算得到收益函数与成本函数并作为返回值返回
        pass

    def findway(self, target:Node) -> List[Node]:
        #D*算法，得到路径序列
        pass