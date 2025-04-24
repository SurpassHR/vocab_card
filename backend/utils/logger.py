import logging
import sys

# ANSI escape codes for colors
COLOR_RESET = "\033[0m"
COLOR_DEBUG = "\033[94m"  # Light Blue
COLOR_INFO = "\033[92m"   # Light Green
COLOR_WARNING = "\033[93m" # Light Yellow
COLOR_ERROR = "\033[91m"   # Light Red
COLOR_CRITICAL = "\033[95m" # Light Magenta

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        level_color = {
            logging.DEBUG: COLOR_DEBUG,
            logging.INFO: COLOR_INFO,
            logging.WARNING: COLOR_WARNING,
            logging.ERROR: COLOR_ERROR,
            logging.CRITICAL: COLOR_CRITICAL
        }.get(record.levelno, COLOR_RESET)

        record.levelname = f"{level_color}{record.levelname}{COLOR_RESET}"
        return logging.Formatter.format(self, record)

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        formatter = ColoredFormatter(fmt=f'{COLOR_DEBUG}' + '{asctime}' + f'{COLOR_RESET}' + ' ' +
                                     '{filename}:{lineno} {levelname}\t {message}', style="{")
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

    def getLogger(self):
        return self.logger

if __name__ == "__main__":
    # 创建一个 StreamHandler，将日志输出到控制台
    handler = logging.StreamHandler(sys.stdout)

    # 创建一个 ColoredFormatter 并设置给 handler
    formatter = ColoredFormatter(fmt='%(asctime)s - %(levelname)s - %(message)s', style="%")
    handler.setFormatter(formatter)

    # 获取 root logger 并添加 handler
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)  # 设置 root logger 的级别

    logging.debug("这是一条调试信息")
    logging.info("这是一条普通信息")
    logging.warning("这是一条警告信息")
    logging.error("这是一条错误信息")
    logging.critical("这是一条严重错误信息")