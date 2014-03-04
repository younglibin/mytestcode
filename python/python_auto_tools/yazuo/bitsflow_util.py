#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import os
import subprocess
from util.login import *


class BitsflowUtil(Login):
    bitsflow_home = None
    cmd = ''

    def __init__(
            self,
            login_info,
            username=None,
            password=None,
            thread_num=6,
    ):
        Login.__init__(self, login_info, username, password, thread_num)
