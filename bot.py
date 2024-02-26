import os
import json

from botScheduler import *
from config import app

from satori import Event
from satori.client import Account
import plugins
from plugins.SendBnStatusToGroup import update_bn_status
from plugins.SendMapDataToGroup import update_map_status


@app.register
async def listen(account: Account, event: Event):
    print(account, event)
    print('')


@scheduler.scheduled_job('interval', minutes=10)
async def _():
    await update_map_status()
    await update_bn_status()


if __name__ == '__main__':
    if not os.path.exists('mapdata.json'):
        with open('mapdata.json', 'w') as f:
            new_data = []  # 新數據
            f.write(json.dumps(new_data))

    if not os.path.exists('bnstatus.json'):
        with open('bnstatus.json', 'w') as f:
            new_data = []  # 新數據
            f.write(json.dumps(new_data))

    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            new_data = {
                "group":
                    {
                        "std": [],
                        "ctb": [],
                        "mania": [],
                        "taiko": [],
                        "mapping": [],
                        "bn":
                            {
                                "std": [],
                                "ctb": [],
                                "mania": [],
                                "taiko": []
                            }
                    }
            }
            f.write(json.dumps(new_data))

    app.run()
