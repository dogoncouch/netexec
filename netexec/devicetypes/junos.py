# MIT License
# 
# Copyright (c) 2020 Dan Persons <dpersonsdev@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from netexec.devicetypes.type import DeviceTypeModule as OurModule

class DeviceTypeModule(OurModule):
    def __init__(self, user=None, password=None, timeout=45):
        """Initialize a device type module"""
        # Module information for help menus, etc
        self.name = 'junos'
        self.desc = 'juniper networks junos'

        self.user = user
        self.password = password
        self.timeout = timeout
        self.usernamerex = r'Username:' # regex for username prompt
        self.passwordrex = r'Password:' # regex for password prompt

        self.prompts = {
                'exec': r'[a-zA-Z0-9\.\-_]+@[a-zA-Z0-9\.\-_]+>\s?',
                'config': r'[a-zA-Z0-9\.\-_]+@[a-zA-Z0-9\.\-_]+#\s?',
                'shell': r'[a-zA-Z0-9\.\-_]+@\S+:RE:.\%'
                } # prompts the program can expect to see
        self.promptoptions = list(self.prompts.values())

        self.disablepaging = [
                'set cli screen-length 0',
                'set cli screen-width 1000'
                ] # commands to disable paging
        self.configcommand = 'configure private'
        self.preconfigcommands = None
        self.postconfigcommands = ['show | compare']
        self.commitcommand = 'commit and-quit'
        # configquit isn't needed, since 'commit and-quit' quits config mode
        self.configquitcommand = None
        self.exitcommands = ['exit']


    #def configure(self):
    #    """Enter lines in config mode"""
    #    # This method should enter config mode, run preconfig, enter lines,
    #    # and run postconfig. If the device type has the ability to
    #    # commit changes, they should not be committed.
    #    pass


    #def execute(self):
    #    """Just enter all the lines"""
    #    # This method should just enter lines, and accept any of the
    #    # available prompts.
    #    pass
