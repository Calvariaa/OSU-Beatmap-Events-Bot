from satori import WebsocketsInfo
from satori.client import App

# rename this file to config.py

app = App(WebsocketsInfo(host="", port=5500, token=""))

BOTACCOUNT = 12345
SUPERUSERS = {12345, 123456}
COMMAND_START = "-"
DEBUG = False
