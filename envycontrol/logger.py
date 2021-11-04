import logging as log
import envs

log.basicConfig(level=log.DEBUG,
                format='%(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                handlers=[
                    log.FileHandler(envs.LOG_FILE_PATH, encoding='utf-8'),
                    log.StreamHandler()
                ])

if __name__ == '__main__':
    log.debug('Prueba debug')
    log.info('Prueba info')
    log.warning('Prueba warning')
    log.error('Prueba error')
    log.critical('Prueba critico')
