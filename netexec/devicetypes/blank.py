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
        self.name = ''
        self.desc = ''

        # Uncomment and change these to modify them from the defaults:

        #self.user = user
        #self.password = password
        #self.timeout = timeout
        #self.usernamerex = r'Username:' # regex for username prompt
        #self.passwordrex = r'Password:' # regex for password prompt
        #self.prompts = {} # prompts the program can expect to see

        #self.disablepaging = [] # commands to disable paging

        #self.configcommand = ''
        #self.preconfigcommand = None
        #self.postconfigcommand = None
        #self.commitcommand = None
        #self.configquit = ''
        #self.exitcommand = ''


        # You can define custom connect(), configure(), and exec() commands here.
        # Use the ones in type.py for reference, that is what you inherit by default.
