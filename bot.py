import os
import json

from config import app

from satori import Event
from satori.client import Account
import plugins


@app.register
async def listen(account: Account, event: Event):
    print(account, event)

if __name__ == '__main__':
    if not os.path.exists('mapdata.json'):
        with open('mapdata.json', 'w') as f:
            new_data = []  # 新數據
            f.write(json.dumps(new_data))

    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            new_data = {"group": {"std": [], "ctb": [], "mania": [], "taiko": [], "mapping": []}}
            f.write(json.dumps(new_data))

    app.run()
