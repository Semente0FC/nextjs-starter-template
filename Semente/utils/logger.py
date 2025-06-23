import logging
import os

def setup_logger(log_file="seemente.log"):
    logger = logging.getLogger("Semente")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
