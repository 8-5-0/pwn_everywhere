import logging
from logging import handlers


logger = logging.getLogger('Pwn management')
formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(threadName)s][%(funcName)s] %(message)s")


console_handle  = logging.StreamHandler()
console_handle.setLevel(logging.DEBUG)
console_handle.setFormatter(formatter)


logger.addHandler(console_handle)

