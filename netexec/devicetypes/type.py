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

from os import environ
from sys import exit
from time import sleep
import pexpect
import re

class DeviceTypeModule:
    def __init__(self):
        """Initialize a device type module"""
        # Module information for help menus, etc
        self.name = ''
        self.desc = ''

        self.user = user
        self.password = password
        self.timeout = timeout
        self.usernamerex = r'Username:' # regex for username prompt
        self.passwordrex = r'Password:' # regex for password prompt

        self.prompts = {
                'exec': r'[a-z\-\._]+@[a-zA-Z0-9\.\-_]+(?:>|#)\s?',
                'config': r'[a-z\-\._]+@[a-zA-Z0-9\.\-_]+#\s?',
                'shell': r'[a-z\-\._]+@[a-zA-Z0-9\.\-_]+(?:>|#)\s?'
                } # prompts the program can expect to see
        self.promptoptions = list(self.prompts.values())

        self.disablepaging = [] # commands to disable paging

        self.configcommand = ''
        self.preconfigcommands = None # None or a list containing preconfiguration commands
        self.postconfigcommands = None # None or a list, like above
        self.commitcommand = None
        self.configquitcommand = None
        self.exitcommands = ['exit']


    def configure(self, commands=None, commit=False):
        """Enter lines in config mode"""
        # This method should enter config mode, run preconfig, enter lines,
        # and run postconfig. If the device type has the ability to
        # commit changes, they should not be committed.
        try:
            if self.configcommand:
                self.px.sendline(self.configcommand)
                self.px.expect(self.prompts['config'], timeout=self.timeout)
                print(self.px.before.decode('utf-8'))
                sleep(0.8)
            if self.preconfigcommands:
                for line in self.preconfigcommands:
                    self.px.sendline(line)
                    self.px.expect(self.prompts['config'], timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)
            if commands:
                for line in commands:
                    self.px.sendline(line)
                    self.px.expect(self.prompts['config'], timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)
            if self.postconfigcommands:
                for line in self.postconfigcommands:
                    self.px.sendline(line)
                    self.px.expect(self.prompts['config'], timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)
            if commit:
                # Commit config
                if self.commitcommand:
                    self.px.sendline(self.commitcommand)
                    self.px.expect(self.promptoptions, timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)
                # Exit config mode, if needed
                if self.configquitcommand:
                    self.px.sendline(self.configquitcommand)
                    self.px.expect(self.promptoptions, timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)
                # Disconnect from the device
                for line in self.exitcommands:
                    self.px.sendline(line)
                    self.px.expect(self.promptoptions, timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)
            else:
                print('\n==== Interactive mode ====' + \
                        '\nPress enter for a prompt.')
                self.px.interact()

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
            try:
                print(self.px.before.decode('utf-8'))
            except(Exception):
                pass
            print('==== EOF: Disconnected ====')
            return()


    def execute(self, commands=None):
        """Just enter all the lines"""
        # This method should just enter lines, and accept any of the
        # available prompts.
        try:
            if commands:
                for line in commands:
                    self.px.sendline(line)
                    self.px.expect(self.promptoptions, timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)
            print('\n==== Interactive mode ====' + \
                    '\nPress enter for a prompt.')
            self.px.interact()

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


    def connect(self, device=None, user=None, password=None, timeout=45,
            command='ssh', sendyes=False):
        """Initiate a connection"""
        # Connect to the device
        try:
            myenv = environ.copy()
            if self.user:
                # Set up connection command
                commandline = 'bash -ic "' + command + ' ' + \
                        self.args.user + '@' + device + '"'
            else:
                commandline = 'bash -ic "' + command + ' ' + \
                        device + '"'
            self.px = pexpect.spawn(commandline, env=myenv,
                        timeout=self.timeout)
            # Send 'yes' to verify host key, if option is enabled
            if sendyes:
                sleep(5)
                verifymsg = 'Are you sure you want to continue ' + \
                        'connecting (yes/no)?'
                if self.px.before:
                    if verifymsg in self.px.before.decode('utf-8'):
                        self.px.sendline('yes')
            
            if self.password:
                self.px.expect(self.passwordrex, timeout=self.timeout)
                print(self.px.before.decode('utf-8'))
                self.px.sendline(self.password)
            self.px.expect(self.promptoptions, timeout=self.timeout)
            print(self.px.before.decode('utf-8'))
            sleep(0.8)

            # Disable screen paging and stuff
            if self.disablepaging:
                for line in self.disablepaging:
                    self.px.sendline(line)
                    self.px.expect(self.promptoptions, timeout=self.timeout)
                    print(self.px.before.decode('utf-8'))
                    sleep(0.8)

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

