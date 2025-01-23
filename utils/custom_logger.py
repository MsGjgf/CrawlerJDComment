# _*_ coding : utf-8 _*_
# @Time : 2024/10/28 21:15
# @Author : 哥几个佛
# @File : custom_logger
# @Project : CrawlerJDComment
import logging

import colorlog


# 配置日志的函数
def setup_logging():
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    handler.setFormatter(formatter)

    logger = colorlog.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


# 调用配置日志的函数，获取可直接使用的日志记录器
logger = setup_logging()

# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
