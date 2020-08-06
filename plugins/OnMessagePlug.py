import json
import time
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

from plugins import getData
from plugins import getUser

def dataToString(data):
    s = ''
    if data['mapstatus'] == 'ranked':
        s += '∑ (Ranked)'
    if data['mapstatus'] == 'loved':
        s += '❤ (Loved)'
    if data['mapstatus'] == 'qualify':
        s += 'Ω (Qualified)'
    if data['mapstatus'] == 'nominate':
        s += '💭 (Nominated)'
    if data['mapstatus'] == 'nomination-reset':
        s += '💥 (Popped)'
    if data['mapstatus'] == 'disqualify':
        s += '💔 (Disqualified)'
    if 'mode' in data:
        m = data['mode']
        mode_std = m % 2
        mode_taiko = int(m/2) % 2
        mode_ctb = int(m/4) % 2
        mode_mania = int(m/8)
        if mode_std != 0:
            s += ' ⭕'
        if mode_taiko != 0:
            s += ' 🥁'
        if mode_ctb != 0:
            s += ' 🍎'
        if mode_mania != 0:
            s += ' 🎹'
    s += '\n' + data['maptitle'] + '(' + data['mapurl'] + ')\n' + data['info']
    return s

def ifExisted(data, old_data):
    for d in old_data:
        if d["time"] != data["time"]:
            continue
        if d["maptitle"] != data["maptitle"]:
            continue
        if d["mapstatus"] != data["mapstatus"]:
            continue
        return True
    return False

@nonebot.scheduler.scheduled_job('interval', minutes=0.1)
async def update_map_status():
    bot = nonebot.get_bot()
    mapdata = open('mapdata.json', 'r')
    old_data = mapdata.read()
    old_data = json.loads(old_data)
    mapdata.close()

    list = getUser.getUsers()
    groups_std = list['group']['std']
    groups_ctb = list['group']['ctb']
    groups_mania = list['group']['mania']
    groups_taiko = list['group']['taiko']
    groups_mapping = list['group']['mapping']

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
        time.sleep(2)
        if not ifExisted(d, old_data):
            old_data.append(d)
        
            m = d['mode']
            mode_std = m % 2
            mode_taiko = int(m/2) % 2
            mode_ctb = int(m/4) % 2
            mode_mania = int(m/8)
            
            mode_mapping = 0
            if not d['mapstatus'] == 'ranked':
                mode_mapping = 1
        
            if mode_std != 0 and mode_mapping != 1:
                for group in groups_std:
                    time.sleep(0.5)
                    try:
                        await bot.send_group_msg(group_id=group, message=dataToString(d))
                    except CQHttpError:
                        pass
                        
            if mode_ctb != 0 and mode_mapping != 1:
                for group in groups_ctb:
                    time.sleep(0.5)
                    try:
                        await bot.send_group_msg(group_id=group, message=dataToString(d))
                    except CQHttpError:
                        pass
                        
            if mode_mania != 0 and mode_mapping != 1:
                for group in groups_mania:
                    time.sleep(0.5)
                    try:
                        await bot.send_group_msg(group_id=group, message=dataToString(d))
                    except CQHttpError:
                        pass
                        
            if mode_taiko != 0 and mode_mapping != 1:
                for group in groups_taiko:
                    time.sleep(0.5)
                    try:
                        await bot.send_group_msg(group_id=group, message=dataToString(d))
                    except CQHttpError:
                        pass
                        
            if mode_mapping == 1:
                for group in groups_mapping:
                    time.sleep(0.5)
                    try:
                        await bot.send_group_msg(group_id=group, message=dataToString(d))
                    except CQHttpError:
                        pass
            
    with open('./mapdata.json', "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()
        f.write(json.dumps(new_data))
