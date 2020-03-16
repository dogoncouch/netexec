#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2020 Dan Persons (dpersonsdev@gmail.com)
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

from argparse import ArgumentParser
from sys import exit
from os import environ
from getpass import getpass
import pexpect
import re
from time import sleep
from os.path import isfile


__version__ = '0.1'


class NetExecCore:

    def __init__(self):
        """Initialize the program"""

        self.args = None
        self.types = {}
        self.types['junos'] = {}
        self.types['junos']['promptrex'] = r'\n[a-z_]+@[a-zA-Z0-9\.\-_]+>\s?'
        self.types['junos']['configpromptrex'] = r'[a-z_]+@[a-zA-Z0-9\.-]+#\s?'
        self.types['junos']['usernamerex'] = r'Username:'
        self.types['junos']['passwordrex'] = r'Password:'


    def get_args(self):
        """Set argument options"""

        parser = ArgumentParser()
        parser.add_argument('--version', action = 'version',
                version = '%(prog)s ' + str(__version__))
        parser.add_argument('-y',
                action = 'store_true', dest = 'yes',
                help = 'send "yes" for host key check (not recommended)')
        parser.add_argument('-u',
                action = 'store', dest = 'user',
                help = 'set a username')
        parser.add_argument('-p',
                action = 'store_true', dest = 'password',
                help = 'use a password (will prompt; DO NOT enter as arg)')
        parser.add_argument('-c',
                action = 'store', dest = 'command', default = 'ssh',
                help = 'command to connect (default ssh)')
        parser.add_argument('-x', '--exec-mode',
                action = 'store_true', dest = 'execmode',
                help = 'enter lines in exec mode, instead of config mode')
        parser.add_argument('-d',
                action = 'store', dest = 'devicetype', default = 'junos',
                help = 'set the device type (junos, ios, etc)')
        deviceparser = \
                parser.add_mutually_exclusive_group(required = True)
        deviceparser.add_argument('--list-types',
                action = 'store_true', dest = 'list_types',
                help = 'list available device types')
        parser.add_argument('-i',
                action = 'store', dest = 'input',
                help = 'set the input file for commands')
        parser.add_argument('-t',
                action = 'store', dest = 'timeout', type = int, default = 45,
                help = 'set the timeout for spawning and sending lines')
        deviceparser.add_argument('-l',
                action = 'store', dest = 'devicelist',
                help = 'connect to all devices in specified list file')
        deviceparser.add_argument('device', action='store', nargs = '?',
                help='specify a device to which to connect')

        self.args = parser.parse_args()


    def setup(self):
        """Set variables"""

        # If --list-types option was used, list types and exit
        if self.args.list_types:
            print('==== Device types ====')
            for key in self.types.keys():
                print(key)
            exit(0)

        # If -p option was used, ask the user for a password
        if self.args.password:
            self.password = getpass('Password:')

        # Set up device type
        # To do: read device types from JSON formatted modules
        if self.args.devicetype in self.types:
            self.promptrex = self.types[self.args.devicetype]['promptrex']
            self.configpromptrex = \
                    self.types[self.args.devicetype]['configpromptrex']
            self.usernamerex = self.types[self.args.devicetype]['usernamerex']
            self.passwordrex = self.types[self.args.devicetype]['passwordrex']
        else:
            print('Device type ' + self.args.devicetype + \
                    ' not recognized.\nTry --list-types option.')

        # Set up device list
        self.devicelist = []
        if self.args.devicelist:
            self.read_devices()
            pass
        else:
            self.devicelist.append(self.args.device)
        if self.args.input:
            self.read_input()


    def read_devices(self):
        """Read lines from device list file"""

        if self.args.devicelist:
            if isfile(self.args.devicelist):
                with open(self.args.devicelist, 'r') as f:
                    self.devicelist = [x.rstrip() for x in f.readlines()]
            else:
                print('Device list file not found: ' + \
                        self.args.devicelist + '.')
                exit(1)
        else:
            print('No input file specified; going interactive right away.')


    def read_input(self):
        """Read lines from input file to execute on devices"""

        if self.args.input:
            if isfile(self.args.input):
                with open(self.args.input, 'r') as f:
                    self.lines = [x.rstrip() for x in f.readlines()]
            else:
                print('Input command file not found: ' + self.args.input + '.')
                exit(1)
        else:
            print('No input file specified; going interactive right away.')


    def config_mode(self):
        """Set up promt, etc for config mode"""
        pass

    def exec_mode(self):
        """Set up prompt, etc for exec mode"""
        pass

    def shell_mode(self):
        """Set up prompt, etc for shell mode"""
        pass


    def connect(self, device):
        """Connect to a device and do stuff"""

        try:
            # Connect to the device
            try:
                myenv = environ.copy()
                if self.args.user:
                    # Set up connection command
                    commandline = 'bash -ic "' + self.args.command + ' ' + \
                            self.args.user + '@' + device + '"'
                else:
                    commandline = 'bash -ic "' + self.args.command + ' ' + \
                            device + '"'
                px = pexpect.spawn(commandline, env=myenv,
                            timeout=self.args.timeout)
                # Send 'yes' to verify host key, if option is enabled
                if self.args.yes:
                    sleep(5)
                    verifymsg = 'Are you sure you want to continue ' + \
                            'connecting (yes/no)?'
                    if px.before:
                        if verifymsg in px.before.decode('utf-8'):
                            px.sendline('yes')
                if self.args.password:
                    px.expect(self.passwordrex, timeout=self.args.timeout)
                    px.sendline(self.password)
            except pexpect.exceptions.TIMEOUT:
                print('Connection timed out.')
                return()

            if self.args.devicetype == 'junos' and self.args.user == 'root':
                # Expect juniper root prompt and enter junos CLI
                px.expect(r'root\@\S+:RE:.\%')
                print(px.before.decode('utf-8'))
                px.sendline('cli')

            # To do: change logic, expect list of things to cover junos root,
            # verify message, etc.
            # To Do: use custom function instead of expecting prompt to cover
            # multiple prompt types
            px.expect(self.promptrex, timeout=self.args.timeout)
            print(px.before.decode('utf-8'))

            # Disable screen paging and screen wrap
            px.sendline('set cli screen-length 0')
            px.expect(self.promptrex, timeout=self.args.timeout)
            print(px.before.decode('utf-8'))
            px.sendline('set cli screen-width 1000')
            px.expect(self.promptrex, timeout=self.args.timeout)
            print(px.before.decode('utf-8'))
            
            if self.args.execmode:
                # Enter lines in exec mode
                if self.args.input:
                    for line in self.lines:
                        px.sendline(line)
                        if self.args.user == 'root' and \
                                line == 'exit':
                            # Exit through root prompt
                            # This can be removed when new logic is implemented
                            px.expect(r'root\@\S+:RE:.\%')
                            print(px.before.decode('utf-8'))
                            print('Exiting')
                            px.sendline('exit')
                        else:
                            px.expect(self.promptrex,
                                    timeout=self.args.timeout)
                            print(px.before.decode('utf-8'))
                            sleep(0.2)

                print('==== Interactive mode ====\nPress enter for a prompt.')
                px.interact()
            
            else:
                # Enter config mode, and enter lines
                # To do: take out if/then, use dictionary for config command
                if self.args.devicetype == 'junos':
                    px.sendline('configure')
                elif self.args.devicetype == 'cisco':
                    px.sendline('conf t')
                px.expect(self.configpromptrex, timeout=self.args.timeout)
                print(px.before.decode('utf-8'))
                px.sendline('rollback 0')
                px.expect(self.configpromptrex, timeout=self.args.timeout)
                print(px.before.decode('utf-8'))
                if self.args.input:
                    for line in self.lines:
                        px.sendline(line)
                        if line in ['commit and-quit', 'end']:
                            # Special case for exiting config mode
                            # This can be removedwhen new logic is implemented
                            # Can expect exec prompt after, already in list
                            px.expect(self.promptrex,
                                    timeout=self.args.timeout)
                            print(px.before.decode('utf-8'))
                            print('Exiting')
                            px.sendline('exit')
                            if self.args.user == 'root' and \
                                    self.args.devicetype == 'junos':
                                # Exit through shell if user is root
                                px.expect(r'root\@\S+:RE:.\%')
                                print(px.before.decode('utf-8'))
                                print('Exiting')
                                px.sendline('exit')
                                return()
                        else:
                            px.expect(self.configpromptrex,
                                    timeout=self.args.timeout)
                            print(px.before.decode('utf-8'))
                            sleep(0.2)
                    if self.args.devicetype == 'junos':
                        px.sendline('show | compare')
                        px.expect(self.configpromptrex,
                                timeout=self.args.timeout)
                        print(px.before.decode('utf-8'))
                print('==== Interactive mode ====\nPress enter for a prompt.')
                px.interact()

        except(KeyboardInterrupt):
            # If user hits ctrl-c, go interactive.
            print('==== KeyboardInterrupt ====' + \
                    '\n==== Interactive mode ====' + \
                    '\nPress enter for a prompt.')
            px.interact()
        except(pexpect.exceptions.TIMEOUT):
            # Move to next device on timeout
            print('==== Timeout: Moving on ====')
            return()
        except pexpect.EOF:
            # Move to next device on disconnect
            print('==== EOF: Disconnected ====')
            return()


    def main_event(self):
        """Connect to each device in the list"""

        for device in self.devicelist:
            self.connect(device)


    def run_script(self):
        """Run the whole program"""

        try:
            self.get_args()
            self.setup()
            self.main_event()

        except KeyboardInterrupt:
            print('\nExiting on KeyboardInterrupt')


def main():
    thing = NetExecCore()
    thing.run_script()


if __name__ == "__main__":
    main()
