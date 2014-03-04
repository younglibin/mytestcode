#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cmd import Cmd
import os

import threading
import time
import traceback
from bitsflow_util import BitsflowUtil
from util.load_module import *
import util.login as yoyo_login


class BitsflowTest(Cmd, BitsflowUtil):
    prompt = '[yoyo-sh]> '
    intro = \
        """Welcome to yoyo-shell, please use 'help' to show all commands!

"""
    intro += 'Follow me to install bitsflow:\n'
    intro += '  1) prepare yoyopkg-xxx-noarch.tar.gz\n'
    intro += \
        "  2) run 'install_yoyopkg /home/zhangtao/yoyopkg-xxx-noarch.tar.gz'\n"
    intro += "  3) run 'yoyopkg install --tag BITSFLOW_2_3_1'\n"
    intro += \
        '  4) prepare agent.xml.sample and yoyo.lic in current path\n'
    intro += "  5) run 'config_bitsflow agent.xml.sample yoyo.lic'\n"
    intro += "  6) run 'start_agent'\n"
    intro += "  7) run 'ps'\n"

    def __init__(self, config_file, api=True):
        Cmd.__init__(self)
        self.config = load(config_file)
        BitsflowUtil.__init__(
            self,
            self.config.pc_list,
            self.config.username,
            self.config.password,
            len(self.config.pc_list),
        )

    def do_EOF(self, user_input):
        print 'Bye!'
        return True

    def do_quit(self, user_input):
        """Quit yoyo-shell"""
        return self.do_EOF(user_input)

    def do_q(self, user_input):
        """Quit yoyo-shell"""

        return self.do_quit(user_input)

    def emptyline(self):
        pass

    def do_shell(self, line):
        '''Run a shell command'''

        output = os.popen(line).read()
        print output

    def do_single_cmd(self, user_input):
        """Usage: single_cmd ip cmdStr"""

        inputs = user_input.split()
        if len(inputs) < 2:
            print """Usage: single_cmd ip cmdStr"""
        else:
            outputs = self.single_execute(inputs[0],
                                          ' '.join(inputs[1:]))
            for output in outputs:
                print output.strip()

    def do_parallel_cmd(self, user_input):
        """Usage: parallel_cmd cmdStr"""

        inputs = user_input.split()
        if len(inputs) < 1:
            print """Usage: parallel_cmd cmdStr"""
        else:
            self.parallel_execute(' '.join(inputs[0:]), result_callback=self.print_result)

    def do_serial_cmd(self, user_input):
        """Usage: serial_cmd cmdStr"""

        inputs = user_input.split()
        if len(inputs) < 1:
            print """Usage: serial_cmd cmdStr"""
        else:
            self.serial_execute(' '.join(inputs[0:]))

    def do_ps(self, user_input):
        """Usage: ps [processName] (If no processName, we'll "ps agent")"""

        if len(user_input) == 0:
            cmd = 'ps aux|grep agent'
        else:
            cmd = 'ps aux|grep %s' % user_input
        self.serial_execute(cmd)

    def do_get_file(self, user_input):
        """Usage: get_file remote_file [local_file] """

        inputs = user_input.split()
        if len(inputs) < 1:
            print 'Usage: get_file remote_file [local_file]'
        else:
            if len(inputs) == 2:
                remote_file = inputs[0]
                local_file = inputs[1]
            else:
                remote_file = inputs[0]
                local_file = os.path.basename(inputs[0])
            self.get_file(remote_file, local_file)

    def do_put_file(self, user_input):
        """Usage: put_file local_file [remote_file]"""

        inputs = user_input.split()
        if len(inputs) < 1:
            print """Usage: put_file local_file [remote_file]"""
        else:
            remote_file = local_file = inputs[0]
            if len(inputs) == 2:
                remote_file = inputs[1]
            self.put_file(local_file, remote_file)

if __name__ == '__main__':
    argv = sys.argv
    argn = len(argv)
    if argn == 1:
        config_file = 'config.py'
    elif argn == 2:
        config_file = argv[1]
    else:
        print 'Usage: python %s [config_file]' % argv[0]
        sys.exit(0)

    print 'load config file: ' + config_file
    global bfctl
    bfctl = BitsflowTest(config_file)

    bfctl.cmdloop()
