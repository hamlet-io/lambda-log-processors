import logging
from abc import ABC


LOGGER = logging.getLogger(__name__)


class Sink(ABC):

    def __init__(self):
        pass
