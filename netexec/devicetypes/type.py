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
    def __init__(self, user=None, password=None, timeout=45):
        """Initialize a device type module"""
        # Module information for help menus, etc
        self.name = ''
        self.desc = ''

        self.usernamerex = r'Username:' # regex for username prompt
        self.passwordrex = r'Password:' # regex for password prompt
        self.prompts = {
                'exec': r'[a-z_]+@[a-zA-Z0-9\.\-_]+(?:>|#)\s?',
                'config': r'[a-z_]+@[a-zA-Z0-9\.-_]+#\s?',
                'shell': r'[a-z_]+@[a-zA-Z0-9\.\-_]+(?:>|#)\s?'
                } # prompts the program can expect to see

        self.disablepaging = [] # commands to disable paging

        self.configcommand = ''
        self.preconfigcommands = None # None or a list containing preconfiguration commands
        self.postconfigcommands = None # None or a list, like above
        self.commitcommand = None
        self.configquit = ''
        self.exitcommand = 'exit'


    def configure(self, configcommands=None, timeout=45):
        """Enter lines in config mode"""
        # This method should enter config mode, run preconfig, enter lines,
        # and run postconfig. If the device type has the ability to
        # commit changes, they should not be committed.
        try:
            if self.preconfigcommands:
                for line in self.preconfigcommands:
                    self.px.sendline(line)
                    self.px.expect(self.prompts['config'], timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
            if configcommands:
                for line in configcommands:
                    self.px.sendline(line)
                    self.px.expect(self.prompts['config'], timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
            if self.postconfigcommands:
                for line in self.postconfigcommands:
                    self.px.sendline(line)
                    self.px.expect(self.prompts['config'], timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))

    except(KeyboardInterrupt):
        # If user hits ctrl-c, go interactive.
        print('==== KeyboardInterrupt ====' + \
                '\n==== Interactive mode ====' + \
                '\nPress enter for a prompt.')
        self.px.interact()
    except(pexpect.exceptions.TIMEOUT):
        # Move to next device on timeout
        print('==== Timeout: Moving on ====')
        return()
    except(pexpect.EOF):
        # Move to next device on disconnect
        print('==== EOF: Disconnected ====')
        return()
        pass


    def execute(self, commands=None):
        """Just enter all the lines"""
        # This method should just enter lines, and accept any of the
        # available prompts.
        try:
            if commands:
                for line in commands:
                    self.px.sendline(line)
                    self.px.expect(self.prompts.values(), timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))

    except(KeyboardInterrupt):
        # If user hits ctrl-c, go interactive.
        print('==== KeyboardInterrupt ====' + \
                '\n==== Interactive mode ====' + \
                '\nPress enter for a prompt.')
        self.px.interact()
    except(pexpect.exceptions.TIMEOUT):
        # Move to next device on timeout
        print('==== Timeout: Moving on ====')
        return()
    except(pexpect.EOF):
        # Move to next device on disconnect
        print('==== EOF: Disconnected ====')
        return()


    def connect(self):
        """Initiate a connection"""
        # Connect to the device
        try:
            myenv = environ.copy()
            if self.user:
                # Set up connection command
                commandline = 'bash -ic "' + self.args.command + ' ' + \
                        self.args.user + '@' + device + '"'
            else:
                commandline = 'bash -ic "' + self.args.command + ' ' + \
                        device + '"'
            self.px = pexpect.spawn(commandline, env=myenv,
                        timeout=self.timeout)
            # Send 'yes' to verify host key, if option is enabled
            if self.args.yes:
                sleep(5)
                verifymsg = 'Are you sure you want to continue ' + \
                        'connecting (yes/no)?'
                if self.px.before:
                    if verifymsg in self.px.before.decode('utf-8'):
                        self.px.sendline('yes')
            
            if self.args.password:
                self.px.expect(self.passwordrex, timeout=self.timeout)
                print(self.px.before.decode('utf-8'))
                self.px.sendline(self.password)
            self.px.expect(self.prompts.values(), timeout=self.timeout)
            print(self.px.before.decode('utf-8'))

            # Disable screen paging and stuff
            if self.disablepaging:
                for line in self.disablepaging:
                    self.px.sendline(line)
                    self.px.expect(self.prompts.values(), timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))

        except(KeyboardInterrupt):
            # If user hits ctrl-c, go interactive.
            print('==== KeyboardInterrupt ====' + \
                    '\n==== Interactive mode ====' + \
                    '\nPress enter for a prompt.')
            self.px.interact()
        except(pexpect.exceptions.TIMEOUT):
            # Move to next device on timeout
            print('==== Timeout: Moving on ====')
            return()
        except(pexpect.EOF):
            # Move to next device on disconnect
            print('==== EOF: Disconnected ====')
            return()

