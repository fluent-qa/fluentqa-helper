import typer

from .api_capture import capture
from .mac_proxy_cli import proxy_switch_app

# overall app
app = typer.Typer()

app.add_typer(proxy_switch_app, name="mac-proxy")
app.add_typer(capture, name="capture")


def main():
    app()


if __name__ == '__main__':
    main()
