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

class DeviceTypeModule:
    def __init__(self):
        """Initialize a device type module"""
        # Module information for help menus, etc
        self.name = ''
        self.desc = ''

        self.usernamerex = r'Username:' # regex for username prompt
        self.passwordrex = r'Password:' # regex for password prompt
        self.prompts = {} # possible prompts (regex)

        self.disablepaging = [] # commands to disable paging

        self.configcommand = ''
        self.preconfigcommand = None
        self.postconfigcommand = None
        self.commitcommand = None
        self.configquit = ''
        self.exitcommand = 'exit'


        def configure(self):
            """Enter lines in config mode"""
            # This method should enter config mode, run preconfig, enter lines,
            # and run postconfig. If the device type has the ability to
            # commit changes, they should not be committed.


        def execute(self):
            """Just enter all the lines"""
            # This method should just enter lines, and accept any of the
            # available prompts.
