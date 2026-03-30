import logging
import colorlog
from ansible_easy.scripts.env import runtime

logger = logging.getLogger()
level = getattr(logging, runtime.log_level, logging.INFO)
logger.setLevel(level)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)


file_handler = logging.FileHandler(f"{runtime.log_file_path}/{runtime.log_file_name}")
file_handler.setLevel(level)
file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(console_handler)
