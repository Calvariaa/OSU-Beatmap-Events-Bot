import asyncio
import json
import random

from config import app

from plugins.GetMapData import get_nominate_data_v2
from plugins.GetBotUsers import get_users

from botScheduler import *


def data_to_string(data):
    s = ''
    if data['mapstatus'] == 'ranked':
        s += '⏫ (Ranked)'
    if data['mapstatus'] == 'loved':
        s += '❤️ (Loved)'
    if data['mapstatus'] == 'qualify':
        s += '✅ (Qualified)'
    if data['mapstatus'] == 'nominate':
        s += '💭 (Nominated)'
    if data['mapstatus'] == 'nomination-reset':
        s += '💥 (Popped)'
    if data['mapstatus'] == 'disqualify':
        s += '💔 (Disqualified)'
    if 'mode' in data:
        m = data['mode']
        mode_std = m % 2
        mode_taiko = int(m / 2) % 2
        mode_ctb = int(m / 4) % 2
        mode_mania = int(m / 8)
        if mode_std != 0:
            s += ' ⭕'
        if mode_taiko != 0:
            s += ' 🥁'
        if mode_ctb != 0:
            s += ' 🍎'
        if mode_mania != 0:
            s += ' 🎹'
    s += '\n' + data['maptitle'] + '(' + data['mapurl'] + ')\n' + data['info']
    # title = data['maptitle']
    # s = data['mapstatus'][:1] + ' ' + title.split(' - ')[0][:3] + ('..' if len(title.split(' - ')[0]) > 3 else '') + ' - ' + title.split(' - ')[1].split(' by ')[0][:6] + ('..' if len(title.split(' - ')[1].split(' by ')[0]) > 6 else '') + ' by ' + title.split(' - ')[1].split(' by ')[1][:4] + ('..' if len(title.split(' - ')[1].split(' by ')[1]) > 4 else '')
    print(s)
    return s


def if_existed(data, old_data):
    for d in old_data:
        if d["time"] != data["time"]:
            continue
        if d["maptitle"] != data["maptitle"]:
            continue
        if d["mapstatus"] != data["mapstatus"]:
            continue
        return True
    return False


@scheduler.scheduled_job('interval', minutes=15)
async def _():
    await update_map_status()


async def update_map_status():
    account = list(app.accounts.values())[0]
    try:
        with open('mapdata.json', 'r') as map_data:
            old_data = map_data.read()
            old_data = json.loads(old_data)
    except Exception as e:
        old_data = []

    user_list = get_users()
    groups_std = user_list['group']['std']
    groups_ctb = user_list['group']['ctb']
    groups_mania = user_list['group']['mania']
    groups_taiko = user_list['group']['taiko']
    groups_mapping = user_list['group']['mapping']

    new_data = get_nominate_data_v2()

    remove_list = []
    for d in new_data:
        for d2 in new_data:
            if d['hash'] == d2['hash'] and d['mapstatus'] == 'nominate' and d2['mapstatus'] == 'qualify':
                remove_list.append(d2)
                d['mapstatus'] = 'qualify'
    for item in remove_list:
        new_data.remove(item)

    for d in new_data:
        if not if_existed(d, old_data):
            old_data.append(d)

            m = d['mode']
            mode_std = m % 2
            mode_taiko = int(m / 2) % 2
            mode_ctb = int(m / 4) % 2
            mode_mania = int(m / 8)

            mode_mapping = 0
            if d['mapstatus'] != 'ranked' and d['mapstatus'] != 'loved':
                mode_mapping = 1

            await asyncio.sleep(5)

            if mode_mapping == 1:
                for group in groups_mapping:
                    await asyncio.sleep(1)
                    print("Send {} to Group {}".format(str(d), group))
                    await account.session.send_message(channel=group, message=data_to_string(d))
            else:
                if mode_std != 0:
                    for group in groups_std:
                        await asyncio.sleep(1)
                        print("Send {} to Group {}".format(str(d), group))
                        await account.session.send_message(channel=group, message=data_to_string(d))

                if mode_ctb != 0:
                    for group in groups_ctb:
                        await asyncio.sleep(1)
                        print("Send {} to Group {}".format(str(d), group))
                        await account.session.send_message(channel=group, message=data_to_string(d))

                if mode_mania != 0:
                    for group in groups_mania:
                        await asyncio.sleep(1)
                        print("Send {} to Group {}".format(str(d), group))
                        await account.session.send_message(channel=group, message=data_to_string(d))

                if mode_taiko != 0:
                    for group in groups_taiko:
                        await asyncio.sleep(1)
                        print("Send {} to Group {}".format(str(d), group))
                        await account.session.send_message(channel=group, message=data_to_string(d))

    with open('mapdata.json', "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()
        f.write(json.dumps(new_data))
