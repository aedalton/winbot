# pylint: disable=missing-docstring

import logging


def get_logger(name, stream_handler_name="APP"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handlers = [h.name for h in logger.handlers]
    if stream_handler_name not in handlers:
        handler = logging.StreamHandler()
        handler.set_name(stream_handler_name)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
