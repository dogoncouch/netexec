# netexec

## Usage

### Options
```
usage: netexec [-h] [--version] [-y] [-u USER] [-p] [-c COMMAND] [-x]
               [-d DEVICETYPE] [--list-types] [-i INPUT] [-t TIMEOUT]
               [-l DEVICELIST]
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
  -d DEVICETYPE    set the device type (junos, ios, etc)
  --list-types     list available device types
  -i INPUT         set the input file for commands
  -t TIMEOUT       set the timeout for spawning and sending lines
  -l DEVICELIST    connect to all devices in specified list file
```

## Examples
    
    netexec -u root -p -i inputcommands.txt 10.50.50.1
    netexec --list-types

## Notes
This doesn't work yet.

## Support
Bugs, questions, and other issues can be directed to the project's [issues page](https://github.com/dogoncouch/netexec/issues) on GitHub, or emailed to [dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com).

## Contributing
Contributions are welcome in the form of code, bug fixes, or testing feedback. For more on how to contribute to netexec, see the [code of conduct](docs/CODE_OF_CONDUCT.md) and [contributing guielines](docs/CONTRIBUTING.md).


# Copyright
MIT License

Copyright (c) 2020 Dan Persons (dpersonsdev@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
