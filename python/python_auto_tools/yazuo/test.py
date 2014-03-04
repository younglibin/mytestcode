#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from cmd import Cmd
import os
current_path = os.path.split(os.path.realpath(__file__))[0]
print current_path
sys.path.append(os.path.join(current_path, "..",""))
sys.path.append(os.path.join(current_path, "..",'','..',''))
import threading
import time
import traceback
from util.load_module import *
import util.login as login
bfctl = None
class Monitor(threading.Thread):
    def __init__(
            self,
            remote,
            environ_conf,
            plugin_conf,
    ):
        global REMOTE_SCRIPT_HOME
        self.remote = remote
        self.plugin_conf = plugin_conf
        self.environ_conf = environ_conf
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self._disable = threading.Event()
        #add class level parameter
        self.plugins = dict()
        self._disable.set()
        self.start()
    def run(self):
        while self._disable.isSet():
            time.sleep(5)
        #self.plugins = dict()
        for (key, val) in vars(self.plugin_conf).iteritems():
            if key.startswith('__') and key.endswith('__'):
                continue
            else:
                importStr = 'from plugin import *'
                exec importStr
                plugin = eval('%s.%s(self.environ_conf, val)' % (val['module'], val['class']))
                self.plugins[key] = plugin
                crontab = plugin.get_crontab()
                pc_list = plugin.get_pc_list()
                create_crontab = "%s '%s'" \
                                 % (self.yoyo_join(REMOTE_SCRIPT_HOME, 'crontab.sh'),
                                    crontab)
                # print create_crontab
                self.remote.serial_execute(create_crontab, pc_list)
        while True:
            if self._disable.isSet():
                time.sleep(30)
            else:
                for (k, v) in self.plugins.iteritems():
                    pc_list = v.get_pc_list()
                    output_file = v.get_output()
                    cmd = 'cat %s' % output_file
                    return_outputs = \
                        self.remote.parallel_execute(cmd, pc_list, self.remote.collect_result)
                    for (pc, outputs) in return_outputs.iteritems():
                        length = ''
                        for output in outputs:
                            length += output.rstrip()
                        if len(length) != 0:
                            print '======== monitor[%s] report[%s] ========' \
                                  % (k, pc)
                            for output in outputs:
                                print output.rstrip('\n')
                time.sleep(30)
    def enable(self):
        self._disable.clear()
        print 'Monitor has been enabled...'
    def disable(self):
        self._disable.set()
        print 'Monitor has been disabled...'
class Test(Cmd,login):
    prompt = '[yoyo-sh]> '
    intro =  """Welcome to yoyo-shell, please use 'help' to show all commands!"""

    def __init__(self, config_file):
        Cmd.__init__(self)
        self.config = load(config_file)

    	login.__init__(
				'yazuo',
				self.config.pc_list,
				self.config.username,
				self.config.password,
				len(self.config.pc_list)
		)
 

    def do_EOF(self, user_input):
        print 'Bye!'
        return True
    def do_quit(self, user_input):
        """Quit yoyo-shell"""
        self.unregister_crontab()
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

    def yoyo_join(self, path1, *args):
        if (len(args) > 0 ):
            for arg in args:
                path1 += "/%s"%arg
        return path1

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
    bfctl = Test(config_file)
    
    bfctl.cmdloop()
