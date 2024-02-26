from satori import Event
from satori.client import Account

from plugins.SendMapDataToGroup import update_map_status
import plugins.GetBotUsers

from botCommand import on_command


# @on_request('friend')
# async def _(session: RequestSession):
#     await session.approve()
#     return
#
#
# @on_request('group')
# async def _(session: RequestSession):
#     await session.approve()
#     return


@on_command('sub_help')
async def _(account: Account, event: Event):
    await account.session.send_message(event.channel.id,
                                       "订阅看实时飞图状态和取消订阅，订阅-sub_MODE，取消订阅-unsub。\n ps:MODE可选：std,ctb,taiko,mania")


@on_command('sub_update')
async def _(account: Account, event: Event):
    await account.session.send_message(event.channel.id, "checking")
    await update_map_status()
    await account.session.send_message(event.channel.id, "updated")


@on_command('ping')
async def _(account: Account, event: Event):
    await account.session.send_message(event.channel.id,"pong")


@on_command('sub_std')
async def _(account: Account, event: Event):
    list = plugins.getUser.get_users()
    #    mode = session.get()

    if event.channel is not None and event.channel.id in list['group']['std']:
        await account.session.send_message(event.channel.id, '本群已经订阅！')
        return

    if event.channel is not None and event.channel.id not in list['group']['std']:
        list['group']['std'].append(event.channel.id)
        await account.session.send_message(event.channel.id, '订阅成功！')
        plugins.getUser.save_users(list)


@on_command('sub_ctb')
async def _(account: Account, event: Event):
    list = plugins.getUser.get_users()
    #    mode = session.get()

    if event.channel is not None and event.channel.id in list['group']['ctb']:
        await account.session.send_message(event.channel.id, '本群已经订阅！')
        return

    if event.channel is not None and event.channel.id not in list['group']['ctb']:
        list['group']['ctb'].append(event.channel.id)
        await account.session.send_message(event.channel.id, '订阅成功！')
        plugins.getUser.save_users(list)


@on_command('sub_mania')
async def _(account: Account, event: Event):
    list = plugins.getUser.get_users()
    #    mode = session.get()

    if event.channel is not None and event.channel.id in list['group']['mania']:
        await account.session.send_message(event.channel.id, '本群已经订阅！')
        return

    if event.channel is not None and event.channel.id not in list['group']['mania']:
        list['group']['mania'].append(event.channel.id)
        await account.session.send_message(event.channel.id, '订阅成功！')
        plugins.getUser.save_users(list)


@on_command('sub_taiko')
async def _(account: Account, event: Event):
    list = plugins.getUser.get_users()
    #    mode = session.get()

    if event.channel is not None and event.channel.id in list['group']['taiko']:
        await account.session.send_message(event.channel.id, '本群已经订阅！')
        return

    if event.channel is not None and event.channel.id not in list['group']['taiko']:
        list['group']['taiko'].append(event.channel.id)
        await account.session.send_message(event.channel.id, '订阅成功！')
        plugins.getUser.save_users(list)


@on_command('sub_mapping')
async def _(account: Account, event: Event):
    list = plugins.getUser.get_users()
    #    mode = session.get()

    if event.channel is not None and event.channel.id in list['group']['mapping']:
        await account.session.send_message(event.channel.id, '本群已经订阅！')
        return

    if event.channel is not None and event.channel.id not in list['group']['mapping']:
        list['group']['mapping'].append(event.channel.id)
        await account.session.send_message(event.channel.id, '订阅成功！')
        plugins.getUser.save_users(list)


@on_command('sub_all')
async def _(account: Account, event: Event):
    list = plugins.getUser.get_users()
    #    mode = session.get()

    sendstr = ''

    if event.channel is not None and event.channel.id in list['group']['std']:
        sendstr += 'std本群已经订阅！' + '\n'
    if event.channel is not None and event.channel.id not in list['group']['std']:
        list['group']['std'].append(event.channel.id)
        sendstr += 'std订阅成功！' + '\n'

    if event.channel is not None and event.channel.id in list['group']['ctb']:
        sendstr += 'ctb本群已经订阅！' + '\n'
    if event.channel is not None and event.channel.id not in list['group']['ctb']:
        list['group']['ctb'].append(event.channel.id)
        sendstr += 'ctb订阅成功！' + '\n'

    if event.channel is not None and event.channel.id in list['group']['mania']:
        sendstr += 'mania本群已经订阅！' + '\n'
    if event.channel is not None and event.channel.id not in list['group']['mania']:
        list['group']['mania'].append(event.channel.id)
        sendstr += 'mania订阅成功！' + '\n'

    if event.channel is not None and event.channel.id in list['group']['taiko']:
        sendstr += 'taiko本群已经订阅！'
    if event.channel is not None and event.channel.id not in list['group']['taiko']:
        list['group']['taiko'].append(event.channel.id)
        sendstr += 'taiko订阅成功！'

    await account.session.send_message(event.channel.id, sendstr)
    plugins.getUser.save_users(list)


# unsub

@on_command('unsub')
async def _(account: Account, event: Event):
    list = plugins.getUser.get_users()

    sendstr = ''
    if event.channel is not None and event.channel.id not in list['group']['std']:
        sendstr += 'std本群已不在订阅！' + '\n'
    if event.channel is not None and event.channel.id in list['group']['std']:
        list['group']['std'].remove(event.channel.id)
        sendstr += 'std已取消订阅！' + '\n'

    if event.channel is not None and event.channel.id not in list['group']['ctb']:
        sendstr += 'ctb本群已不在订阅！' + '\n'
    if event.channel is not None and event.channel.id in list['group']['ctb']:
        list['group']['ctb'].remove(event.channel.id)
        sendstr += 'ctb已取消订阅！' + '\n'

    if event.channel is not None and event.channel.id not in list['group']['mania']:
        sendstr += 'mania本群已不在订阅！' + '\n'
    if event.channel is not None and event.channel.id in list['group']['mania']:
        list['group']['mania'].remove(event.channel.id)
        sendstr += 'mania已取消订阅！' + '\n'

    if event.channel is not None and event.channel.id not in list['group']['taiko']:
        sendstr += 'taiko本群已不在订阅！' + '\n'
    if event.channel is not None and event.channel.id in list['group']['taiko']:
        list['group']['taiko'].remove(event.channel.id)
        sendstr += 'taiko已取消订阅！' + '\n'

    if event.channel is not None and event.channel.id not in list['group']['mapping']:
        sendstr += 'mapping本群已不在订阅！'
    if event.channel is not None and event.channel.id in list['group']['mapping']:
        list['group']['mapping'].remove(event.channel.id)
        sendstr += 'mapping已取消订阅！'

    await account.session.send_message(event.channel.id, sendstr)

    plugins.getUser.save_users(list)
