#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

log_level = logging.DEBUG
log_name = "yoyo_shell.log"

#don't change it
logger = logging.getLogger("qa")
logger.setLevel(log_level)
loggerch = logging.StreamHandler()
loggerfile = logging.FileHandler(log_name)
loggerch.setLevel(log_level)
loggerformatter = logging.Formatter("%(asctime)s - %(module)s(%(lineno)d): %(message)s")
loggerch.setFormatter(loggerformatter)
loggerfile.setFormatter(loggerformatter)
logger.addHandler(loggerch)
logger.addHandler(loggerfile)


