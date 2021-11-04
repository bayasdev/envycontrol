import logging as log
from envs import LOG_FILE_PATH

log.basicConfig(level=log.DEBUG,
                format='%(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                handlers=[
                    log.FileHandler(LOG_FILE_PATH, encoding='utf-8'),
                    log.StreamHandler()
                ])
