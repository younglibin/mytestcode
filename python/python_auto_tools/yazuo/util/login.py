#!/usr/bin/python
# -*- coding: utf-8 -*-

import ssh
import sys
import os
import threading
import time
import traceback
import platform

from threadpool import ThreadPool
from threadpool import makeRequests

IS_LINUX = False
#import signal 
operation_platform=platform.system()
if operation_platform =='Windows':
    IS_LINUX = False
else:
    IS_LINUX = True
print IS_LINUX

login_pclist = []
login_connections = {}


class Login:

    def __init__(
        self,
        login_info,
        username,
        password,
        thread_num,
        ):
        self.thread_num = thread_num
        try:
            if isinstance(login_info, list):
                login_info = list(set(login_info))
                self.username = username
                self.password = password
                self.start_work(self.__create_connection_by_list,
                                login_info)
            elif isinstance(login_info, dict):
                self.login_dict = login_info
                self.start_work(self.__create_connection_by_dict,
                                login_info.keys())
            else:
                raise Exception('login_info must be list or dict')
        except:
            print sys.exc_info()
        finally:
            pass

    def __create_connection_by_dict(self, pc):
        global login_connections
        global login_pclist
        try:
            login_info = self.login_dict[pc].split(':')
            username = login_info[0]
            password = login_info[1]
            connection = ssh.Connection(pc, username, password)
            login_connections[pc] = connection
            login_pclist.append(pc)
            print 'create connection to %s successful.' % pc
        except:
            print sys.exc_info()
            print 'create connection to %s failed.' % pc

    def __create_connection_by_list(self, pc):
        global login_connections
        global login_pclist
        try:
            connection = ssh.Connection(pc, self.username,
                    self.password)
            login_connections[pc] = connection
            login_pclist.append(pc)
            print 'create connection to %s successful.' % pc
        except:
            print sys.exc_info()
            print 'create connection to %s failed.' % pc

    def print_result(self, request, result):
        try:
            getattr(request, "outputs")
            request.outputs[request.args[0]] = result

            print '======== target: %s ========' % request.args[0]
            for output in result:
                print output.rstrip('\n')
            print '================= end =================\n'
        except:
            traceback.print_exc()

    def collect_result(self, request, result):
        try:
            getattr(request, "outputs")
            request.outputs[request.args[0]] = result
        except:
            traceback.print_exc()

    def start_work(
        self,
        work,
        args_list,
        result_callback=None,
        ):
        outputs = dict()
        try:
            requests = makeRequests(work, args_list, result_callback,
                                    None)
            job = ThreadPool(self.thread_num)
            for req in requests:
                req.outputs = outputs
                job.putRequest(req)
            job.wait()
        except:
            traceback.print_exc()
        return outputs

    def single_execute(self, pc, cmd):
        global login_connections
        global login_pclist
        outputs = ''
        if pc in login_connections:
            outputs = login_connections[pc].execute(cmd)
        else:
            print "%s hasn't been initialized." % pc
        return outputs

    def serial_execute(self, cmd, input_pclist=None):
        return self.parallel_execute(cmd, input_pclist, self.print_result)

    def same_execute(self, pc):
        return self.single_execute(pc, self.cmd)

    def parallel_execute(self, cmd, input_pclist=None, result_callback=None):
        global login_pclist
        self.cmd = cmd

        if input_pclist is None:
            pcs = login_pclist
        else:
            pcs = input_pclist

        return self.start_work(self.same_execute, pcs, result_callback)

    def __put_file(self, pc):
        global login_connections
        try:
            login_connections[pc].put(self.local_file, self.remote_file)
        except:
            print 'put_file [%s] to [%s:%s] error.' % (self.local_file,
                    pc, self.remote_file)

    def put_file_to_pc(
        self,
        local_file,
        remote_file,
        pc,
        ):
        global login_connections
        try:
            login_connections[pc].put(local_file, remote_file)
        except:
            print 'put_file [%s] to [%s:%s] error.' % (local_file, pc,
                    remote_file)

    def put_file(self, local_file, remote_file=None):
        global login_pclist
        self.local_file = local_file
        self.remote_file = remote_file
        self.start_work(self.__put_file, login_pclist)

    def __get_file(self, pc):
        global login_connections
        try:
            login_connections[pc].get(self.remote_file, pc + '-'
                    + self.local_file)
        except:
            traceback.print_exc()
            print 'get_file [%s] from [%s] error.' % (self.remote_file,
                    pc)

    def get_file_from_pc(
        self,
        remote_file,
        local_file,
        pc,
        ):
        global login_connections
        try:
            login_connections[pc].get(remote_file, local_file)
        except:
            print 'get_file [%s] from [%s] error.' % (remote_file, pc)

    def get_file(
        self,
        remote_file,
        local_file=None,
        pclist=None,
        ):
        global login_pclist

        self.remote_file = remote_file

        if local_file is None:
            self.local_file = os.path.basename(remote_file)
        else:
            self.local_file = local_file

        if pclist is None:
            pclist = login_pclist

        self.start_work(self.__get_file, pclist)
