from nonebot import on_request, RequestSession, on_command, CommandSession
import plugins.getUser

@on_request('friend')
async def _(session: RequestSession):
    await session.approve()
    return

@on_request('group')
async def _(session: RequestSession):
    await session.approve()
    return

@on_command('help_sub',only_to_me=False)
async def _(session: CommandSession):
    print(session.ctx)
    await session.send("订阅看实时飞图状态和取消订阅，订阅-sub_MODE，取消订阅-unsub，谢谢合作。\n ps:MODE可选：std,ctb,taiko,mania")

@on_command('sub_std',only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()
#    mode = session.get()

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['std']:
        await session.send('本群已经订阅！')
        return

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['std']:
        list['group']['std'].append(session.ctx['group_id'])
        await session.send('订阅成功！')
        plugins.getUser.saveUsers(list)

@on_command('sub_ctb',only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()
#    mode = session.get()

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['ctb']:
        await session.send('本群已经订阅！')
        return

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['ctb']:
        list['group']['ctb'].append(session.ctx['group_id'])
        await session.send('订阅成功！')
        plugins.getUser.saveUsers(list)

@on_command('sub_mania',only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()
#    mode = session.get()

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['mania']:
        await session.send('本群已经订阅！')
        return

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['mania']:
        list['group']['mania'].append(session.ctx['group_id'])
        await session.send('订阅成功！')
        plugins.getUser.saveUsers(list)

@on_command('sub_taiko',only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()
#    mode = session.get()

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['taiko']:
        await session.send('本群已经订阅！')
        return

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['taiko']:
        list['group']['taiko'].append(session.ctx['group_id'])
        await session.send('订阅成功！')
        plugins.getUser.saveUsers(list)

@on_command('sub_mapping',only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()
#    mode = session.get()

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['mapping']:
        await session.send('本群已经订阅！')
        return

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['mapping']:
        list['group']['mapping'].append(session.ctx['group_id'])
        await session.send('订阅成功！')
        plugins.getUser.saveUsers(list)

@on_command('sub_all',only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()
#    mode = session.get()

    sendstr = ''

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['std']:
        sendstr += 'std本群已经订阅！' + '\n'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['std']:
        list['group']['std'].append(session.ctx['group_id'])
        sendstr += 'std订阅成功！' + '\n'

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['ctb']:
        sendstr += 'ctb本群已经订阅！' + '\n'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['ctb']:
        list['group']['ctb'].append(session.ctx['group_id'])
        sendstr += 'ctb订阅成功！' + '\n'

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['mania']:
        sendstr += 'mania本群已经订阅！' + '\n'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['mania']:
        list['group']['mania'].append(session.ctx['group_id'])
        sendstr += 'mania订阅成功！' + '\n'

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['taiko']:
        sendstr += 'taiko本群已经订阅！'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['taiko']:
        list['group']['taiko'].append(session.ctx['group_id'])
        sendstr += 'taiko订阅成功！'
        
    await session.send(sendstr)
    plugins.getUser.saveUsers(list)

#unsub

@on_command('unsub',only_to_me=False)
async def _(session: CommandSession):
    list = plugins.getUser.getUsers()

    
    sendstr = ''
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['std']:
        sendstr += 'std本群已不在订阅！' + '\n'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['std']:
        list['group']['std'].remove(session.ctx['group_id'])
        sendstr += 'std已取消订阅！' + '\n'

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['ctb']:
        sendstr += 'ctb本群已不在订阅！' + '\n'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['ctb']:
        list['group']['ctb'].remove(session.ctx['group_id'])
        sendstr += 'ctb已取消订阅！' + '\n'

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['mania']:
        sendstr += 'mania本群已不在订阅！' + '\n'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['mania']:
        list['group']['mania'].remove(session.ctx['group_id'])
        sendstr += 'mania已取消订阅！' + '\n'

    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['taiko']:
        sendstr += 'taiko本群已不在订阅！' + '\n'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['taiko']:
        list['group']['taiko'].remove(session.ctx['group_id'])
        sendstr += 'taiko已取消订阅！' + '\n'
        
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] not in list['group']['mapping']:
        sendstr += 'mapping本群已不在订阅！'
    if session.ctx['message_type'] == 'group' and session.ctx['group_id'] in list['group']['mapping']:
        list['group']['mapping'].remove(session.ctx['group_id'])
        sendstr += 'mapping已取消订阅！'
        
    await session.send(sendstr)

    plugins.getUser.saveUsers(list)
