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
import netexec.devicetypes
import gettext
gettext.install('netexec')


__version__ = '0.1'


class NetExecCore:

    def __init__(self):
        """Initialize the program"""
        self.args = None
        self.devicetypes = {}


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
        modeparser = parser.add_mutually_exclusive_group()
        modeparser.add_argument('-x', '--exec-mode',
                action = 'store_true', dest = 'execmode',
                help = 'enter lines in exec mode, instead of config mode')
        modeparser.add_argument('--commit',
                action = 'store_true',
                help = 'commit config and exit (no interactive mode')
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
        # If -p option was used, ask the user for a password
        if self.args.password:
            self.password = getpass('Password:')
        else:
            self.password = None

        # Set up device list
        self.devicelist = []
        if self.args.devicelist:
            self.read_devices()
        else:
            self.devicelist.append(self.args.device)
        if self.args.input:
            self.read_input()


    def list_devicetypes(self, *args):
        """Return a list of available parsing modules"""
        print('==== Available parsing modules: ====\n')
        for devicetype in sorted(self.devicetypes):
            print(self.devicetypes[devicetype].name.ljust(16) + \
                ': ' + self.devicetypes[devicetype].desc)
        exit(0)
    
    def load_devicetypes(self):
        """Load parsing module(s)"""
        for devicetype in sorted(netexec.devicetypes.__all__):
            self.devicetypes[devicetype] = \
                __import__('netexec.devicetypes.' + devicetype, globals(), \
                locals(), [netexec]).DeviceTypeModule()


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
            print('No input file specified; will go interactive right away.')


    def connect_devices(self):
        """Connect to devices and execute"""
        con = self.devicetypes[self.args.devicetype]
        for device in self.devicelist:
            con.connect(device, user=self.args.user, password=self.password,
                    timeout=self.args.timeout, command=self.args.command)
            if self.args.execmode:
                con.execute(commands=self.lines)
            else:
                con.configure(commands=self.lines, commit=self.args.commit)


    def run_script(self):
        """Run the whole program"""
        try:
            self.get_args()
            self.setup()
            self.load_devicetypes()
            if self.args.list_types:
                self.list_devicetypes()
            else:
                self.connect_devices()

        except KeyboardInterrupt:
            print('\nExiting on KeyboardInterrupt')


def main():
    thing = NetExecCore()
    thing.run_script()


if __name__ == "__main__":
    main()
