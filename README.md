# FluentQA Simple Capture

***Only Support Python3.10*** because of mimtproxy compatitable issue.


- [zh-intro](README-zh.md)

For Some Reason,I want to try to capture API to generate tests,
but don't want to spend too much time on this.

What I want:

- Use as less code as you can to capture API request to database for automation code generation.
- A simple UI to do the proxy setting and start capturing API Request.

Finally, after doing some research,I completed it in one day.
Features:

1. cli to start mitmproxy and plugin
2. cli to reset proxy
3. ui to start mitmproxy,plugin and reset proxy

## Commandline Features:

- Use mitmproxy to capture API request:

```shell
poetry run qacli capture start --name="scenario_name"
```

![start.png](start.png)

- Capture API Request Based on Configuration: configs/settings.toml

captured URL setting: all request to www.baidu.com and www.bing.com will save to database

```shell
mitm = { recorded_url = "https://www.baidu.com,https://www.bing.com" }
```

- all api request and response in database, table fields:

```python
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

```

- turn on/off proxy setting in MAC

```shell
 poetry run qacli mac-proxy --help
                                                                                                                                                         
 Usage: qacli mac-proxy [OPTIONS] COMMAND [ARGS]...                                                                                                      
                                                                                                                                                         
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ off                  disable api capture proxy                                                                                                        │
│ on                   enable api capture proxy 
```

- capture/record in CLI manner

```shell
❯ poetry run qacli capture --help

api recorder initialized ....
                                                                                                                                                                                                                   
 Usage: qacli capture [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                  
                                                                                                                                                                                                                   
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ start                                                  capture api                                                                                                                                              │
│ stop                                                   stop capture api                                                                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```

## UI Feature

```shell
poetry run qaui
```

![qaui.png](qaui.png)

- input capture name: any name your want
- start to capture API request
- Query Database to get all the request you want

```sql
select * from api_monitor_record where scenario_name=<your_record_name>
```

- export or do some changes for your automation testing

## To Do

- [X] [后台管理录制数据](https://github.com/fluent-qa/fluentqa-workspace)
- [X] [接口数据下载](https://github.com/fluent-qa/fluentqa-workspace)
- [X] 下载数据修改后直接用于自动化测试
- [X] postman 接口数据管理
- [X] Code Generation

## Installation


```sh
ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" uv pip install mitmproxy
# ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" uv add mitmproxy
```