import logging

logger = logging.getLogger()

logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
fmt = logging.Formatter(fmt="%(levelname)s: %(message)s")
handler.setFormatter(fmt)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

