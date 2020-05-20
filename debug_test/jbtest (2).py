from bs4 import BeautifulSoup
import urllib.request
import json
import socket
socket.setdefaulttimeout(60)

url = "https://osu.ppy.sh/beatmapsets/events?types%5B%5D=nominate&types%5B%5D=qualify&types%5B%5D=rank&types%5B%5D=love&types%5B%5D=nomination_reset&types%5B%5D=disqualify"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
jshtml = (soup.find(id="json-events")).string.lstrip()

#print(type(jshtml))
#print (jshtml)
mapjson = json.loads(jshtml)
#print(mapjson[1])

for mapnow in mapjson:
    url = 'https://osu.ppy.sh/beatmapsets/' + str(mapnow['beatmapset']['id'])

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find(id='json-beatmapset').string.lstrip()
    raw_data = json.loads(content)
    title = raw_data['artist']+' - '+raw_data['title'] + ' by '+raw_data['creator']
    mode_data = 0
    # std=1 taiko=2 ctb=4 mania=8
    mode_osu = False
    mode_taiko = False
    mode_ctb = False
    mode_mania = False
    for diff in raw_data['beatmaps']:
        if diff['convert'] == True:
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
    print(title)