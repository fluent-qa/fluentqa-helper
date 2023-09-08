#!/usr/bin/env python
# -*- coding:utf-8 -*-
import asyncio
from asyncio import AbstractEventLoop

import typer
from mitmproxy.options import Options
from mitmproxy.tools.web.master import WebMaster
from pydantic import BaseModel, ConfigDict

from capture import recorder
from capture.recorder import PRecorder
from commands.mac_proxy_cli import proxy_on, proxy_off

capture = typer.Typer(name="capture")


class CaptureServer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    master: WebMaster = None
    status: bool = False
    loop: AbstractEventLoop = None

    async def create_mitmweb(self, name):
        options = Options()
        web_master = WebMaster(options)
        recorder.addons = [PRecorder(record_name=name)]
        web_master.addons.add(recorder)
        self.master = web_master
        await self.master.run()

    def run(self, name):
        self.loop = asyncio.new_event_loop()
        self.status = True
        self.loop.run_until_complete(self.create_mitmweb(name))

    def reload_plugin(self, name):
        self.master.addons.remove(recorder)
        recorder.addons = [PRecorder(record_name=name)]
        self.master.addons.add(recorder)


capture_server = CaptureServer()


@capture.command(name="start", help="capture api")
def start(name: str = typer.Option("name", "--name", help="capture name, example: test")):
    if name is None:
        name = "capture"
    proxy_on()
    # os.system('nohup mitmweb -s capture/recorder.py --set record_name=' + name + " & echo $! > pid")
    if capture_server.master is None:
        capture_server.run(name)
        capture_server.status = True
    else:
        if capture_server.master:
            capture_server.reload_plugin(name)
        else:
            capture_server.run(name)


@capture.command(name="stop", help="stop capture api")
def stop_capture():
    proxy_off()
    capture_server.status = False
    # todo: set value into a file
    # os.system("cat pid | xargs kill -9")
