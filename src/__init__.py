#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

import logging

from src.formatstr import LogStr

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
def log_print(msg):
    logger.debug(msg)

log_str = LogStr()
