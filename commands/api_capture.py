#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import typer

from commands.mac_proxy_cli import proxy_on

capture = typer.Typer(name="capture")


@capture.command(name="start", help="capture api")
def start(name: str = typer.Option("name", "--name", help="capture name, example: test")):
    if name is None:
        name = "capture"
    proxy_on()
    os.system('nohup mitmweb -s capture/recorder.py --set record_name=' + name + " & echo $! > pid")



@capture.command(name="stop", help="stop capture api")
def stop_capture():
    # todo: set value into a file
    os.system("cat pid | xargs kill -9")
