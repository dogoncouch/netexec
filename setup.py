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
"""
Netexec
----------

Netexec is a CLI utility for basic network automation. It can connect to devices, and execute commands to either gather information or make configuration changes.

Options
```````

::

    usage: netexec [-h] [--version] [-y] [-u USER] [-p] [-c COMMAND]
               [-x | --commit] [-d DEVICETYPE] [--list-types] [-i INPUT]
               [-t TIMEOUT] [-l DEVICELIST]
               [device]
    
    positional arguments:
      device           specify a device to which to connect
    
    optional arguments:
      -h, --help       show this help message and exit
      --version        show program's version number and exit
      -y               send "yes" for host key check (not recommended)
      -u USER          set a username
      -p               use a password (will prompt; DO NOT enter as arg)
      -c COMMAND       command to connect (default ssh)
      -x, --exec-mode  enter lines in exec mode, instead of config mode
      --commit         commit config and exit (no interactive mode
      -d DEVICETYPE    set the device type (junos, ios, etc)
      --list-types     list available device types
      -i INPUT         set the input file for commands
      -t TIMEOUT       set the timeout for spawning and sending lines
      -l DEVICELIST    connect to all devices in specified list file
    
    ==== Available parsing modules: ====
    
    blank           : a blank devicetype module
    junos           : juniper networks junos

"""

from setuptools import setup
from os.path import join
from sys import prefix
from netexec import __version__

ourdata = [(join(prefix, 'share/man/man1'), ['docs/netexec.1']),
        (join(prefix, 'share/doc/netexec'), ['README.md',
            'docs/CONTRIBUTING.md', 'LICENSE', 'CHANGELOG.md'])]

setup(name = 'netexec', version = str(__version__),
        description = 'Basic CLI network automation tool',
        long_description = __doc__,
        author = 'Dan Persons', author_email = 'dpersonsdev@gmail.com',
        url = 'https://github.com/dogoncouch/netexec',
        download_url = 'https://github.com/dogoncouch/netexec/archive/v' + str(__version__) + '.tar.gz',
        keywords = ['network-automation', 'networking', 'automation'],
        packages = ['netexec', 'netexec.devicetypes'],
        entry_points = \
                { 'console_scripts': [ 'netexec = netexec.core:main' ]},
        data_files = ourdata,
        classifiers = ["Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: POSIX",
            "Programming Language :: Python",
            "Topic :: System :: Systems Administration"])
