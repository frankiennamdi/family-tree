import logging
import logging.config

from file_finder import FileFinder


class LoggingConfigurator:

    @classmethod
    def configure_logging(cls, logging_ini='logging.ini'):
        """
        Configures logging
        """
        located_at = FileFinder.resolve(logging_ini)
        logging.config.fileConfig(located_at, disable_existing_loggers=False)
