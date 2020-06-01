import logging

from robots.robot import Robot
from robots.maps import PheMap, BarrierMap
from robots.setting import BOT_NUMS

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

phe_map = PheMap()
barrier_map = BarrierMap()
robots = []
robots_init_loc = []
for i in range(BOT_NUMS):
    new_bot_node = barrier_map.get_random_node()
    while new_bot_node.loc() in robots_init_loc:
        new_bot_node = barrier_map.get_random_node()
    robots_init_loc.append((new_bot_node.x, new_bot_node.y))
    robots.append(Robot(new_bot_node, bot_id=BOT_NUMS))
