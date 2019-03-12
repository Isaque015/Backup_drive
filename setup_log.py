import logging
import logging.config

logging.config.fileConfig('conf_log.ini')

logger = logging.getLogger('root')
