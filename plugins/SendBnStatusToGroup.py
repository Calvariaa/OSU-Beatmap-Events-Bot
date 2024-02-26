import asyncio
import json

from datetime import datetime

from config import app

from plugins.GetBnStatus import get_bn_status
from plugins.GetBotUsers import get_users


json_file = "bnstatus.json"


def get_bn_status_by_mode(mode, json_data):
    if mode not in ["std", "ctb", "taiko", "mania"]:
        print("Invalid")
        return
    if mode == "std":
        mode = "osu"
    if mode == "ctb":
        mode = "catch"

    users_list = None
    for item in json_data["allUsersByMode"]:
        if item["_id"] == mode:
            users_list = item["users"]
            break

    user_not_closed_list = []
    if users_list is not None:
        # print("for user in users_list:")
        for user in users_list:
            if "closed" not in user['requestStatus']:
                user_not_closed_list += [user]
                # print(user)

    else:
        print("No users found for {}".format(mode))

    return user_not_closed_list


def user_to_string(user):
    s = ""
    if user['mode'] == "osu":
        s += ' ⭕'
    if user['mode'] == "taiko":
        s += ' 🥁'
    if user['mode'] == "catch":
        s += ' 🍎'
    if user['mode'] == "mania":
        s += ' 🎹'
    s += " {}: {}\n".format(user['groups'].upper(), user['username'])

    datetime_obj = datetime.strptime(user['lastOpenedForRequests'], "%Y-%m-%dT%H:%M:%S.%fZ")
    formatted_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    s += "LastOpen: \n - {}\n".format(str(formatted_time))

    s += "Status: \n - {}\n".format(str(user['requestStatus']))
    s += "Profile: \n - https://osu.ppy.sh/users/{}\n".format(user['username'])

    if "requestLink" in user and user['requestLink'] is not None:
        s += "ReqLink: \n - {}".format(user['requestLink'])

    if "requestInfo" in user:
        request_info = str(user['requestInfo'])
        if len(request_info) > 200 or request_info.count('\n') > 3:
            s += "ReqInfo:\n"
            lines = request_info.split('\n')
            for i, line in enumerate(lines[:3]):
                if line != '':
                    s += "  " + line + "\n"
            if len(lines) > 3:
                s += "  ...\n"

    s += "\nBnSite: \n - https://bn.mappersguild.com/modrequests?id={}".format(user['id'])

    return s


def if_existed(data, old_data):
    if data not in old_data:
        return False
    return True
    # for d in old_data:
    #     if d["time"] != data["time"]:
    #         continue
    #     if d["maptitle"] != data["maptitle"]:
    #         continue
    #     if d["mapstatus"] != data["mapstatus"]:
    #         continue
    #     return True
    # return False


async def update_bn_status():
    print("update_bn_status")
    account = list(app.accounts.values())[0]
    try:
        with open(json_file, 'r') as map_data:
            old_data = map_data.read()
            old_data = json.loads(old_data)
    except Exception as e:
        old_data = []

    user_list = get_users()
    groups_std = user_list['group']['bn']['std']
    groups_ctb = user_list['group']['bn']['ctb']
    groups_mania = user_list['group']['bn']['mania']
    groups_taiko = user_list['group']['bn']['taiko']

    bn_data = get_bn_status()

    opened_bn_data_std = get_bn_status_by_mode("std", bn_data)
    opened_bn_data_ctb = get_bn_status_by_mode("ctb", bn_data)
    opened_bn_data_mania = get_bn_status_by_mode("mania", bn_data)
    opened_bn_data_taiko = get_bn_status_by_mode("taiko", bn_data)
    opened_bn_data_all = opened_bn_data_std + opened_bn_data_ctb + opened_bn_data_mania + opened_bn_data_taiko
    # print(opened_bn_data_all)

    for d in opened_bn_data_all:
        if not if_existed(d, old_data):  # 如果存在的话说明上次获取就已经开q，所以这里获取上次获取时没开q的
            await asyncio.sleep(5)

            if d['mode'] == "osu":
                for group in groups_std:
                    await asyncio.sleep(1)
                    print("Send {} to Group {}".format(str(d), group))
                    await account.session.send_message(channel=group, message=user_to_string(d))

            if d['mode'] == "catch":
                for group in groups_ctb:
                    await asyncio.sleep(1)
                    print("Send {} to Group {}".format(str(d), group))
                    await account.session.send_message(channel=group, message=user_to_string(d))

            if d['mode'] == "mania":
                for group in groups_mania:
                    await asyncio.sleep(1)
                    print("Send {} to Group {}".format(str(d), group))
                    await account.session.send_message(channel=group, message=user_to_string(d))

            if d['mode'] == "taiko":
                for group in groups_taiko:
                    await asyncio.sleep(1)
                    print("Send {} to Group {}".format(str(d), group))
                    await account.session.send_message(channel=group, message=user_to_string(d))

    print("Update BN Status to Group Successfully")
    with open(json_file, "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()
        f.write(json.dumps(opened_bn_data_all))


if __name__ == "__main__":
    json_file = "../bnstatus.json"
    try:
        with open(json_file, 'r') as map_data:
            old_data = map_data.read()
            old_data = json.loads(old_data)
    except Exception as e:
        old_data = []

    # user_list = get_users()
    # groups_std = user_list['group']['bn']['std']
    # groups_ctb = user_list['group']['bn']['ctb']
    # groups_mania = user_list['group']['bn']['mania']
    # groups_taiko = user_list['group']['bn']['taiko']

    bn_data = get_bn_status()

    opened_bn_data_std = get_bn_status_by_mode("std", bn_data)
    opened_bn_data_ctb = get_bn_status_by_mode("ctb", bn_data)
    opened_bn_data_mania = get_bn_status_by_mode("mania", bn_data)
    opened_bn_data_taiko = get_bn_status_by_mode("taiko", bn_data)
    opened_bn_data_all = opened_bn_data_std + opened_bn_data_ctb + opened_bn_data_mania + opened_bn_data_taiko
    # print(opened_bn_data_all)

    for d in opened_bn_data_all:
        if not if_existed(d, old_data):  # 如果存在的话说明上次获取就已经开q，所以这里获取上次获取时没开q的
            # await asyncio.sleep(5)

            print(user_to_string(d))
            # if d['mode'] == "osu":
            #     for group in groups_std:
            #         # await asyncio.sleep(1)
            #         print("Send {} to Group {}".format(str(d), group))
            #         # await account.session.send_message(channel=group, message=user_to_string(d))
            #
            # if d['mode'] == "catch":
            #     for group in groups_ctb:
            #         # await asyncio.sleep(1)
            #         print("Send {} to Group {}".format(str(d), group))
            #         # await account.session.send_message(channel=group, message=user_to_string(d))
            #
            # if d['mode'] == "mania":
            #     for group in groups_mania:
            #         # await asyncio.sleep(1)
            #         print("Send {} to Group {}".format(str(d), group))
            #         # await account.session.send_message(channel=group, message=user_to_string(d))
            #
            # if d['mode'] == "taiko":
            #     for group in groups_taiko:
            #         # await asyncio.sleep(1)
            #         print("Send {} to Group {}".format(str(d), group))
            #         # await account.session.send_message(channel=group, message=user_to_string(d))

    print("Update BN Status to Group Successfully")
    with open(json_file, "r+") as f:
        read_data = f.read()
        f.seek(0)
        f.truncate()
        f.write(json.dumps(opened_bn_data_all))
