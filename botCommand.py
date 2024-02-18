from satori import Event
from satori.client import Account

from config import app
from botScheduler import *

from config import COMMAND_START


def on_command(command_name):
    def decorator(func):
        @app.register
        async def wrapper(account: Account, event: Event):
            if str(event.message.content[0]).startswith(COMMAND_START + command_name):
                await func(account, event)

        return wrapper

    return decorator
