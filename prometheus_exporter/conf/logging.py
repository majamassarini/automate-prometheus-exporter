import logging


def default_logging_configuration(log_directory, logging_level=logging.INFO):
    """
    Default logging configuration for prometheus exporter.

    :param log_directory: directory where log files will be stored
    :param logging_level: logging level (default: INFO)
    :return: logging configuration dictionary
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": logging_level,
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": logging_level,
                "formatter": "default",
                "filename": f"{log_directory}/prometheus_exporter.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 3,
            },
        },
        "root": {"level": logging_level, "handlers": ["console", "file"]},
    }
