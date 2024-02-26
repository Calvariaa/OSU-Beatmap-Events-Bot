from time import sleep
from bs4 import BeautifulSoup
import urllib.request
import json
# import socket
# import socks
#
# # socks.set_default_proxy(socks.HTTP, addr='127.0.0.1', port=7890)
# # socket.socket = socks.socksocket
# socket.setdefaulttimeout(120)


def check_modes(url):
    """
    check mode by url

    :param url:
    :return:
    """
    print('  Checking mods on %s' % url)
    try:
        html = urllib.request.urlopen(url).read()
    except:
        print('Holy shit peppy dont bully me uwu ,,,\n so U should wait for 5 second and Ill retry ,,,')
        sleep(5)
        html = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html, 'lxml')
    content = soup.find(id='json-beatmapset').string.lstrip()
    raw_data = json.loads(content)
    title = raw_data['artist'] + ' - ' + raw_data['title'] + ' by ' + raw_data['creator']
    mode_data = 0
    # std=1 taiko=2 ctb=4 mania=8
    mode_osu = False
    mode_taiko = False
    mode_ctb = False
    mode_mania = False
    for diff in raw_data['beatmaps']:
        if diff['convert']:
            continue
        if diff['mode'] == 'osu':
            mode_osu = True
        if diff['mode'] == 'taiko':
            mode_taiko = True
        if diff['mode'] == 'fruits':
            mode_ctb = True
        if diff['mode'] == 'mania':
            mode_mania = True
    if mode_osu:
        mode_data += 1
    if mode_taiko:
        mode_data += 2
    if mode_ctb:
        mode_data += 4
    if mode_mania:
        mode_data += 8
    return title, mode_data


def get_nominate_data_v2():
    """
    update nominate information

    :return:
    """
    url = 'https://osu.ppy.sh/beatmapsets/events?types%5B%5D=nominate&types%5B%5D=qualify&types%5B%5D=rank&types%5B%5D=love&types%5B%5D=nomination_reset&types%5B%5D=disqualify'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    jsHtml = (soup.find(id="json-events")).string.lstrip()
    jsChecker = (soup.find(id="json-users")).string.lstrip()
    nominate_data = []

    mapJson = json.loads(jsHtml)
    mapChecker = json.loads(jsChecker)

    for mapNow in mapJson:

        mapUrl = 'https://osu.ppy.sh/beatmapsets/' + str(mapNow['beatmapset']['id'])
        mapStatus = 'null'
        if mapNow['type'] == 'rank':
            mapStatus = 'ranked'
        if mapNow['type'] == 'love':
            mapStatus = 'loved'
        if mapNow['type'] == 'qualify':
            mapStatus = 'qualify'
        if mapNow['type'] == 'nominate':
            mapStatus = 'nominate'
        if mapNow['type'] == 'nomination_reset':
            mapStatus = 'nomination-reset'
        if mapNow['type'] == 'disqualify':
            mapStatus = 'disqualify'

        time = mapNow['created_at']

        info = ''
        if 'user_id' in mapNow:
            for checkerId in mapChecker:
                if checkerId['id'] == mapNow['user_id']:
                    if mapStatus == 'nominate':
                        info = 'Nominated by ' + checkerId['username'] + '.'
                    if mapStatus == 'disqualify':
                        info = 'Disqualified by ' + checkerId['username'] + '.'
                        if 'discussion' in mapNow:
                            info += '\n' + mapNow['discussion']['starting_post']['message']
        mapModes = check_modes(mapUrl)
        data = {"mapurl": mapUrl, "maptitle": mapModes[0], "mode": mapModes[1],
                "mapstatus": mapStatus, "time": time, "info": info, "hash": hash(time)}
        print("    " + str(data))
        nominate_data.append(data)
    nominate_data.reverse()
    return nominate_data


if __name__ == '__main__':
    d = get_nominate_data_v2()
    print('Final Version:\n')
    print("  " + str(d))
