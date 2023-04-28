#!/usr/bin/env python
import json
from typing import Optional
from mitmproxy.addonmanager import Loader
from mitmproxy.http import HTTPFlow
from mitmproxy import ctx
from sqlmodel import SQLModel, Field

from qpydao import *
from qpybase import settings

db_client = DatabaseClient(DatabaseConfig(url=settings.db.url))
init_pg_database(db_client)


def is_captured_url(url: str):
    url_prefix = settings.mitm.recorded_url.split(",")
    for item in url_prefix:
        if len(item) == 0:
            continue
        if url.startswith(item):
            return True
    return False


class ApiMonitorRecord(SQLModel, table=True):
    __tablename__ = "api_monitor_record"

    id: Optional[int] = Field(default=None, primary_key=True)
    app: Optional[str] = None
    service: Optional[str] = None
    api: Optional[str] = None
    path: Optional[str] = None
    request_url: Optional[str] = None
    method: Optional[str] = None
    request_headers: Optional[str] = None
    request_body: Optional[str] = None
    response_headers: Optional[str] = None
    status_code: int
    response_body: Optional[str] = None
    scenario_name: Optional[str] = None


def save_http_flow(flow: HTTPFlow):
    request_header_dict = {}
    for key, value in flow.request.headers.items():
        request_header_dict[key] = value
    path = flow.request.path
    path_list = path.split('/')
    api = path_list[-1]
    service = path_list[1].split('.')[-1]
    app = path_list[1][:len(path_list[1]) - len(service) - 1]

    response_header_dict = {}
    for key, value in flow.response.headers.items():
        response_header_dict[key] = value

    record = ApiMonitorRecord(
        app=app,
        service=service,
        api=api,
        path=flow.request.path,
        request_url=flow.request.url,
        method=flow.request.method,
        request_headers=json.dumps(request_header_dict),
        request_body=flow.request.content,
        response_headers=json.dumps(response_header_dict),
        status_code=flow.response.status_code,
        response_body=flow.response.content,
        scenario_name=ctx.options.record_name
    )
    print(record.json())
    db_client.save(record)


class PRecorder:
    def __init__(self):
        print("api recorder initialized ....")

    def load(self, loader: Loader):
        loader.add_option(
            name="record_name",
            typespec=Optional[str],
            default="capture",
            help="capture name"
        )

    def http_connect(self, flow: HTTPFlow):
        print("http_connect state")

    def requestheaders(self, flow: HTTPFlow):
        print("request headers state")

    def request(self, flow: HTTPFlow):
        pass

    def responseheaders(self, flow: HTTPFlow):
        print("respones headers state")

    def response(self, flow: HTTPFlow):
        """
        extract both request and response
        into local database/sqlite
        then update to center database
        Args:
            flow:

        Returns:

        """
        if is_captured_url(
                flow.request.url) and flow.request.method.lower() != 'options':
            save_http_flow(flow)
            # flow.response.status_code = 502
            # flow.response.content = bytes("Bad Gateway",'utf-8')

    def error(self, flow: HTTPFlow):
        print("error state")

    # def tcp_start(self, flow: TCPFlow):
    #     print("tcp start state")
    #
    # def tcp_message(self, flow: TCPFlow):
    #     print("tcp message state")
    #
    # def tcp_error(self, flow: TCPFlow):
    #     print("tcp error state")
    #
    # def tcp_end(self, flow: TCPFlow):
    #     print("tcp send state")

    # def websocket_handshake(self, flow: HTTPFlow):
    #     print("websocket send state")


addons = [
    PRecorder()
]
