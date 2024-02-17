import asyncio
import json
import time
import random

from config import app, BOTACCOUNT

from plugins import getData
from plugins import getUser

from botScheduler import *


def text_obfuscate(data):
    """
    滚你妈的腾讯,SB

    :param data:
    :return:
    """
    enum = {
        'a': ['a', 'à', 'á', 'â', 'ã', 'ä', 'å', 'ɑ', 'а', 'ạ'],
        'b': ['b', 'ʙ', 'Ь', 'ｂ'],
        'c': ['c', 'ϲ', 'с', 'ⅽ', 'ƈ', 'ċ', 'ć'],
        'd': ['d', 'cl', 'd', 'ԁ', 'ժ', 'ⅾ', 'ｄ', 'ɗ'],
        'e': ['e', 'é', 'ê', 'ë', 'ē', 'ĕ', 'ė', 'ｅ', 'е', 'ẹ', 'ę'],
        'f': ['f', 'Ϝ', 'Ｆ', 'ｆ'],
        'g': ['g', 'ɢ', 'ɡ', 'Ԍ', 'Ԍ', 'ｇ', 'ġ'],
        'h': ['h', 'һ', 'ｈ'],
        'i': ['i', '1', 'l', 'Ꭵ', 'ⅰ', 'ｉ', 'í', 'ï'],
        'j': ['j', 'ј', 'ｊ', 'ʝ'],
        'k': ['k', 'lc', 'κ', 'ｋ'],
        'l': ['l', '1', 'i', 'ⅼ', 'ｌ'],
        'm': ['m', 'nn', 'rn', 'rr', 'ṃ', 'ⅿ', 'ｍ'],
        'n': ['n', 'r1', 'ｎ', 'ń'],
        'o': ['o', '0', 'Ο', 'ο', 'О', 'о', 'Օ', 'Ｏ', 'ｏ', 'ȯ', 'ọ', 'ỏ', 'ơ', 'ó'],
        'p': ['p', 'ρ', 'р', 'ｐ'],
        'q': ['q', 'ｑ', 'զ'],
        'r': ['r', 'ʀ', 'ｒ'],
        's': ['s', 'Ⴝ', 'Ꮪ', 'Ｓ', 'ｓ', 'ʂ', 'ś'],
        't': ['t', 'τ', 'ｔ'],
        'u': ['u', 'μ', 'υ', 'Ս', 'Ｕ', 'ｕ', 'ս'],
        'v': ['v', 'ｖ', 'ѵ', 'ⅴ', 'ν'],
        'w': ['w', 'vv', 'ѡ', 'ｗ'],
        'x': ['x', 'ⅹ', 'ｘ', 'х', 'ҳ'],
        'y': ['y', 'ʏ', 'γ', 'у', 'Ү', 'ｙ', 'ý'],
        'z': ['z', 'ｚ', 'ʐ', 'ż', 'ź', 'ʐ'],
        '/': ['丿', '/', '|'],
        '.': ['。', ',', '、']
    }
    for letter in enum:
        data = data.replace(letter, enum[letter][random.randint(0, len(enum[letter]) - 1)])
    return data


def data_to_string(data):
    s = ''
    if data['mapstatus'] == 'ranked':
        s += '♾️ (Ranked)'
    if data['mapstatus'] == 'loved':
        s += '❤️ (Loved)'
    if data['mapstatus'] == 'qualify':
        s += '✔️ (Qualified)'
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
    account = app.get_account("chronocat/{}".format(BOTACCOUNT))
    try:
        with open('mapdata.json', 'r') as map_data:
            old_data = map_data.read()
            old_data = json.loads(old_data)
    except Exception as e:
        old_data = []

    user_list = getUser.getUsers()
    groups_std = user_list['group']['std']
    groups_ctb = user_list['group']['ctb']
    groups_mania = user_list['group']['mania']
    groups_taiko = user_list['group']['taiko']
    groups_mapping = user_list['group']['mapping']

    new_data = getData.get_nominate_data_v2()

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
            if not d['mapstatus'] == 'ranked':
                mode_mapping = 1

            await asyncio.sleep(5)

            if mode_mapping == 1:
                for group in groups_mapping:
                    await asyncio.sleep(1)
                    await account.session.send_message(channel=group, message=data_to_string(d))
            else:
                if mode_std != 0:
                    for group in groups_std:
                        await asyncio.sleep(1)
                        await account.session.send_message(channel=group, message=data_to_string(d))

                if mode_ctb != 0:
                    for group in groups_ctb:
                        await asyncio.sleep(1)
                        await account.session.send_message(channel=group, message=data_to_string(d))

                if mode_mania != 0:
                    for group in groups_mania:
                        await asyncio.sleep(1)
                        await account.session.send_message(channel=group, message=data_to_string(d))

                if mode_taiko != 0:
                    for group in groups_taiko:
                        await asyncio.sleep(1)
                        await account.session.send_message(channel=group, message=data_to_string(d))

    with open('mapdata.json', "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()
        f.write(json.dumps(new_data))
