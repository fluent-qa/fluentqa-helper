
import typer
import os

proxy = "127.0.0.1"
port = 8080

proxy_switch_app = typer.Typer(name="mac-proxy")


@proxy_switch_app.command(name="on", help="enable api capture proxy")
def proxy_on():
    os.system('networksetup -setwebproxy Wi-Fi ' + proxy + ' ' + str(port))
    os.system('networksetup -setsecurewebproxy Wi-Fi ' + proxy + ' ' + str(port))


@proxy_switch_app.command(name="off", help="disable api capture proxy")
def proxy_off():
    os.system('networksetup -setwebproxystate "Wi-Fi" off')
    os.system('networksetup -setsecurewebproxystate "Wi-Fi" off')
