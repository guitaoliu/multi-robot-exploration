import numpy as np
import random
import logging

from typing import Union, List

from robots.setting import (
    BOT_COMMUNICATE_RANGE,
    BOT_MOVING_RANGE,
    PROFIT_RATIO,
    PHE_RATIO,
    BOT_SENSOR_RANGE,
    MAP_SIZE,
)

import robots
from robots.maps import ExploreMap, PheMap, Node
from robots.a_star import AStar

logger = logging.getLogger(__name__)


class Robot:

    def __init__(self, node: Union[Node, tuple], bot_id: int):
        if isinstance(node, Node):
            self.node = node
        elif isinstance(node, tuple):
            self.node = Node(node)
        else:
            raise TypeError
        self.bot_id = bot_id
        self.moving_range = BOT_MOVING_RANGE
        self.sensor_range = BOT_SENSOR_RANGE
        self.comm_range = BOT_COMMUNICATE_RANGE
        self.loc_barrier_map = ExploreMap()
        self.loc_explore_map = ExploreMap()
        self.moving_path = []
        self.explore_node_list = []

        self.explore()

    def loc(self) -> tuple:
        return self.node.loc()

    def get_moving_profit(self, node: Node) -> float:
        """
        针对任务点的出价函数
        :param node: 任务点
        :return: 出价值，None表示不可达
        """
        if self.get_accessibility(node):
            moving_cost = self.get_manha_distance(node)
            phe = self.get_phe_level(node, robots.phe_map)
            explore_profit = self.get_explore_profit(node)
            r = np.exp(
                PROFIT_RATIO * explore_profit + (1 - PROFIT_RATIO) * (
                        moving_cost + PHE_RATIO * phe
                )
            )
            return r
        else:
            return -1

    def get_manha_distance(self, node: Node) -> int:
        """
        返回自身和目标点之间的曼哈顿距离
        :param node: 另一个点
        :return: 曼哈顿距离
        """
        return np.abs(self.node.x - node.x) + np.abs(self.node.y - node.y)

    def get_phe_level(self, node: Node, phe_map: PheMap) -> float:
        """
        得到信息素水平
        :param node:
        :param phe_map: 全局信息素水平
        :return:
        """
        return phe_map.get_phe(self.node, node)

    def get_explore_profit(self, node: Node) -> int:
        """
        简化处理，考虑到达任务点确认点增加情况
        :param node:
        :return:
        """
        new_explore_node = 0
        for i in range(node.x - self.sensor_range, node.x + self.sensor_range + 1):
            for j in range(node.y - self.sensor_range, node.y + self.sensor_range + 1):
                if 0 <= i < MAP_SIZE[0] and 0 <= j < MAP_SIZE[1]:
                    if self.loc_explore_map.map[i, j] == 0:
                        new_explore_node += 1

        return new_explore_node

    def get_accessibility(self, node: Node) -> bool:
        """
        对任务点的探索可达性
        :param node:
        :return: bool
        """
        # todo 任务点过远问题
        return np.sqrt((self.node.x - node.x) ** 2 + (self.node.y - node.y) ** 2) < self.moving_range

    def update_loc_map(self, bot):
        self.loc_explore_map.map |= bot.loc_explore_map.map
        self.loc_barrier_map.map |= bot.loc_barrier_map.map

    def is_finished(self):
        """
        检验本地探索地图，判断地图探索是否完成
        :return: bool
        """
        return self.loc_explore_map.is_finished()

    def get_await_node(self) -> Node:
        """
        边界点中找寻下一个任务
        :return: 对自己最优任务点
        """
        x, y = self.loc()
        node_list = []
        logger.debug(f'bot #{self.bot_id} with sum of local explore map as {np.sum(self.loc_explore_map.map)}')
        for i in range(x - self.moving_range, x + self.moving_range + 1):
            for j in range(y - self.moving_range, y + self.moving_range + 1):
                if 0 <= i < MAP_SIZE[0] and 0 <= j < MAP_SIZE[1]:
                    distance = np.sqrt(np.power(x - i, 2) + np.power(y - j, 2))
                    if self.loc_explore_map.map[i, j] == 0 and distance <= self.moving_range:
                        # logger.debug(f'get node {i, j} with {self.loc_explore_map.map[i, j]}')
                        node_list.append((Node((i, j)), distance))
    
        if node_list:
            target_node = sorted(node_list, key=lambda k: k[1])[0:4]
            return random.choice(target_node)[0]
        else:
            """
            通信范围内无可探测点
            """
            unexplored_map = np.argwhere(self.loc_explore_map.map == 1)
            barriers = np.argwhere(robots.barrier_map.map == 1)
            await_nodes = [tuple(node) for node in unexplored_map if node not in barriers]
            choice = random.choice(await_nodes)
            logger.debug(f'bot #{self.bot_id} has no near target node!!')
            return Node(choice)

    def release_node_and_wait_for_buyer(self) -> (int, Node):
        """
        拍卖执行过程
        :return: 执行者编号 rob_id
        """

        target = self.get_await_node()
        logger.debug(f'bot #{self.bot_id} find node {target.loc()}')
        target_profit = self.get_moving_profit(target)
        node_list = [(target, target_profit)]
        await_list = [(node, self.get_moving_profit(node)) for node in robots.robots_await_nodes[self.bot_id]]

        node, profit = max(node_list+await_list, key=lambda k: k[1])

        executor = self.bot_id
        for bot in robots.robots_list:
            if bot.bot_id != self.bot_id:
                self.update_loc_map(bot)
                bot.update_loc_map(robots.robots_list[self.bot_id])
                if self.get_accessibility(bot.node):
                    bot_profit = bot.get_moving_profit(node)
                    if bot_profit:
                        if bot_profit > profit:
                            executor = bot.bot_id
                            self.loc_explore_map.map[node.x, node.y] = 1

        if node in robots.robots_await_nodes[self.bot_id]:
            robots.robots_await_nodes[self.bot_id].pop(robots.robots_await_nodes[self.bot_id].index(node))

        return executor, node
    
    def explore(self):
        """
        对探索地图进行更新，传感器范围内探索，移动一个单位后执行，包括未知点探索和信息素更新
        """
        x, y = self.loc()
        # 信息素更新
        robots.phe_map.update_phe(self.node)
        # 探索
        for i in range(x - self.sensor_range, x + self.sensor_range + 1):
            for j in range(y - self.sensor_range, y + self.sensor_range + 1):
                if 0 <= i < MAP_SIZE[0] and 0 <= j < MAP_SIZE[1]:
                    distance = np.sqrt((x - i) ** 2 + (y - j) ** 2)
                    if distance <= self.sensor_range and self.loc_explore_map.map[i, j] == 0:
                        self.loc_explore_map.map[i, j] = 1
                        if robots.barrier_map.map[i, j]:
                            self.loc_barrier_map.map[i, j] = 1
    
    def find_way(self, nodes: List):
        """
        用于找到自身到目标点的移动轨迹
        :param nodes:
        :return:
        """
        if len(nodes) == 1:
            end_node = nodes[0]
        else:
            end_node = max(nodes, key=lambda k: self.get_moving_profit(k))
        for i, node in enumerate(robots.robots_await_nodes[self.bot_id]):
            if node.loc() == end_node.loc():
                robots.robots_await_nodes[self.bot_id].pop(i)
                
        a_star_map = ExploreMap()
        a_star_map.map = self.loc_barrier_map.map & self.loc_explore_map.map
        a_star = AStar(self.node, end_node, a_star_map)
        self.explore_node_list = a_star.run()
        logger.debug(f'bot #{self.bot_id} get path {[node.loc() for node in self.explore_node_list]}')

    def move(self, next_node: Node):
        """
        机器人执行移动，并对移动后的点执行探索，探索包括未知点发现和信息素更新
        :param next_node: 下一个移动点
        :return:
        """
        logger.debug(f'bot #{self.bot_id} move from {self.node.loc()} to {next_node.loc()}')
        logger.debug(f'bot #{self.bot_id} current paht {[node.loc() for node in self.explore_node_list]}')
        self.node = next_node
        self.explore()
        self.moving_path.append(next_node)

    def run(self) -> bool:
        """
        这里的执行过程，判断是否能够进行下一步移动，如果不能移动，重新执行寻路算法，更新移动路径，并重新执行移动
        :return:
        """
        if self.explore_node_list:
            if self.loc_barrier_map.status(self.explore_node_list[0]):
                if len(self.explore_node_list) == 1:
                    self.explore_node_list = []
                    return False
                self.find_way([self.explore_node_list[-1]])
            self.move(self.explore_node_list.pop(0))
            return True
        else:
            return False
