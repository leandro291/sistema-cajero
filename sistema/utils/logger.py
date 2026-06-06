import logging
import os

class Logger():

    _logger_instancia = None

    @classmethod
    def __set_logger(cls):

        if cls._logger_instancia is not None:
            return cls._logger_instancia

        log_directory = 'utils/logs'
        log_filename = 'seguridad_atm.log'

        os.makedirs(log_directory, exist_ok=True)

        logger = logging.getLogger("ATM_Logger")
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            log_path = os.path.join(log_directory, log_filename)
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                fmt='%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        cls._logger_instancia = logger
        return cls._logger_instancia

    @classmethod
    def add_to_log(cls, level: str, message: str):
        try:
            logger = cls.__set_logger()

            level = level.lower()
            if level == "error":
                logger.error(message)
            elif level == "info":
                logger.info(message)
            elif level == "warn":
                logger.warning(message)
            else:
                logger.debug(message)
                
        except Exception as e:
            print(f"Error crítico en el sistema de logs: {e}")