import time
import logging


from robots.setting import BOT_NUMS
from robots import robots

logger = logging.getLogger(__name__)


def main():

    for i in range(BOT_NUMS):
        logger.debug(f'bot #{i} is inited at {robots[i].loc()}')
    start = time.time()

    # while True:
    #     stop = 0
    #
    #     for i in range(BOT_NUMS):
    #         if robots[i].is_finished():
    #             stop = 1
    #             break
    #
    #     if stop == 1:
    #         break

    explorer_time = time.time() - start
    logger.info('{:.2f}s elapsed'.format(explorer_time))


if __name__ == '__main__':
    main()
