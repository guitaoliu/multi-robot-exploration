import time
import logging


from robots.setting import BOT_NUMS
from robots import robots, robots_await_nodes, phe_map, barrier_map

logger = logging.getLogger(__name__)


def main():
    final_map = []

    for i in range(BOT_NUMS):
        logger.debug(f'bot #{i} is inited at {robots[i].loc()}')
    start = time.time()

    while True:
        stop = 0
        for i in range(BOT_NUMS):
            bot = robots[i]
            if robots[i].is_finished():
                stop = 1
                final_map = robots[i].loc_barrier_map
                break

            # 判断是否正在执行移动
            if bot.explore_node_list:
                bot.run(barrier_map, phe_map)
                bot.find_way(robots_await_nodes[i])
                continue

            # 静止状态执行拍卖过程
            while not bot.explore_node_list:
                executor, target_node, robots_await_nodes[i] = bot.release_node_and_wait_for_buyer(
                    robots,
                    current_await_node=robots_await_nodes[i]
                )
                robots_await_nodes[executor].append(target_node)
                if executor == i:
                    bot.find_way(robots_await_nodes[i])
                    bot.run(barrier_map, phe_map)
                    break

        # 信息素挥发
        phe_map.phe_volatilize()

        if stop == 1:
            break

    explorer_time = time.time() - start
    logger.info('{:.2f}s elapsed'.format(explorer_time))
    logger.info('最终障碍物地图为\n')
    print(final_map)


if __name__ == '__main__':
    main()
