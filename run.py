import time
import logging
import tkinter as tk

from robots.setting import MAP_SIZE, ZOOM_SIZE, BOT_NUMS
from robots.maps import ExploreMap
import robots

logger = logging.getLogger(__name__)

window = tk.Tk()
window.title('Demo')
window.geometry('1200x900')


def get_rectangle_loc(x: int, y: int):
    return ZOOM_SIZE * x, ZOOM_SIZE * y, ZOOM_SIZE * (x + 1), ZOOM_SIZE * (y + 1)


canvas = tk.Canvas(window, width=MAP_SIZE[0] * ZOOM_SIZE, height=MAP_SIZE[1] * ZOOM_SIZE)
canvas.pack()

start = time.time()
robot_map = 0

stop = 0


def sim():
    global robot_map
    global start
    global stop
    # global canvas_explore_map
    canvas_explore_map = ExploreMap()
    for i in range(BOT_NUMS):
        if robots.robots_list[i].is_finished():
            stop = 1
            robot_map = i
            robots.final_map = robots.robots_list[i].loc_barrier_map
            break

        # 判断是否正在执行移动
        if robots.robots_list[i].explore_node_list:
            robots.robots_list[i].run()
            continue

        # 静止状态执行拍卖过程
        while not robots.robots_list[i].explore_node_list:
            executor, target_node = robots.robots_list[i].release_node_and_wait_for_buyer()
            robots.robots_await_nodes[executor].append(target_node)
            if executor == i:
                robots.robots_list[i].find_way(robots.robots_await_nodes[i])
                robots.robots_list[i].run()
                break

    for bot in robots.robots_list:
        canvas_explore_map.map |= bot.loc_explore_map.map

    # 信息素挥发
    robots.phe_map.phe_volatilize()

    if stop == 1:
        pass
    canvas.delete('all')
    for x in range(MAP_SIZE[0]):
        for y in range(MAP_SIZE[1]):
            if robots.barrier_map[x, y]:
                canvas.create_rectangle(*get_rectangle_loc(x, y), fill='black')
            elif canvas_explore_map.map[x, y]:
                canvas.create_rectangle(*get_rectangle_loc(x, y), fill='white')
            else:
                canvas.create_rectangle(*get_rectangle_loc(x, y), fill='gray')

    for robot in robots.robots_list:
        canvas.create_rectangle(*get_rectangle_loc(*robot.loc()), fill='green')

    if not stop:
        window.after(100, sim)

    if stop:
        explorer_time = time.time() - start
        logger.info('{:.2f}s elapsed'.format(explorer_time))
        logger.info(f'最终障碍物地图为在机器人 #{robot_map} 上')
        logger.info(f'总步数为 {sum([len(item.moving_path) for item in robots.robots_list])} ')
        logger.info(f'单个机器人移动 {sum([len(item.moving_path) for item in robots.robots_list]) // BOT_NUMS}')


if __name__ == '__main__':
    for i in range(MAP_SIZE[0]):
        for j in range(MAP_SIZE[1]):
            if robots.barrier_map[i, j]:
                canvas.create_rectangle(*get_rectangle_loc(i, j), fill='black')
            else:
                canvas.create_rectangle(*get_rectangle_loc(i, j), fill='gray')

    for bot in robots.robots_list:
        canvas.create_rectangle(*get_rectangle_loc(*bot.loc()), fill='green')

    B = tk.Button(window, text='Begin Simulating', font=('Arial', 12), width=15, height=1, command=sim).pack()
    window.mainloop()

