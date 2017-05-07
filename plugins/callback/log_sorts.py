# (C) 2012, Michael DeHaan, <michael.dehaan@gmail.com>

# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import time
import json
from collections import MutableMapping

from ansible.module_utils._text import to_bytes
from ansible.plugins.callback import CallbackBase



class CallbackModule(CallbackBase):
    """
    sort playbook results into different list files, in _base_path
    """
    CALLBACK_VERSION = 1.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'log_sorts'
    CALLBACK_NEEDS_WHITELIST = True

    TIME_FORMAT="%b %d %Y %H:%M:%S"
    _base_path = "/home/ansible/hosts_log"

    def __init__(self):

        super(CallbackModule, self).__init__()

        if not os.path.exists("/home/ansible/hosts_log"):
            os.makedirs("/home/ansible/hosts_log")

    def log(self, line, category = 'ALL'):
        path = []
        if category == 'FAILED':
            path.append(os.path.join(self._base_path, "FAILED.list"))
        elif category == 'OK':
            path.append(os.path.join(self._base_path, "OK.list"))
        elif category == "UNREACHABLE":
            path.append(os.path.join(self._base_path, 'UNREACHABLE.list'))
        else:
            path.append(os.path.join(self._base_path, "FAILED.list"))
            path.append(os.path.join(self._base_path, "OK.list"))
            path.append(os.path.join(self._base_path, 'UNREACHABLE.list'))
        
        for item in path:
            with open(item, "ab") as fd:
                fd.write(line)
                fd.write('\n')

    def v2_playbook_on_start(self, playbook):
        print(playbook._file_name)
        now = time.strftime(self.TIME_FORMAT, time.localtime())
        line = "play_book start : %(playbook_file)s - %(now)s" % dict(playbook_file = playbook._file_name, now = now)
        print(line)
        self.log(line)
    
    def playbook_on_play_start(self, play_name):
        now = time.strftime(self.TIME_FORMAT, time.localtime())
        line = "play start : %(play_name)s - %(now)s" % dict(play_name = play_name, now = now)
        print(line)
        self.log(line)

    def playbook_on_task_start(self, task_name, is_conditional):
        now = time.strftime(self.TIME_FORMAT, time.localtime())
        line = "task start : %(task_name)s - %(now)s" % dict(task_name = task_name, now = now)
        print(line)
        self.log(line)

    def runner_on_ok(self, host, res):
        self.log(host, 'OK')

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.log(host, 'FAILED')

    def runner_on_skipped(self, host, item=None):
        self.log(host, 'SKIPPED' )

    def runner_on_unreachable(self, host, res):
        self.log(host, 'UNREACHABLE' )

    def runner_on_async_failed(self, host, res, jid):
        self.log(host, 'ASYNC_FAILED' )
    
    def set_play_context(self, play_context):
        self.log('\n' )