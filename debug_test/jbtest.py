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
    print(mapnow['type'])

    mapurl = 'https://osu.ppy.sh/beatmapsets/' + str(mapnow['beatmapset']['id'])
    mapstatus = "null"
    if  mapnow == 1:
        mapstatus = "ranked"
    if mapnow['type'] == 'love':
        mapstatus = "loved"
    if mapnow['type'] == 'qualify':
        mapstatus = "qualify"
    if mapnow['type'] == 'nominate':
        mapstatus = "nominate"
    if mapnow['type'] == 'nomination':
        mapstatus = "nomination-reset"
    if mapnow['type'] == 'disqualify':
        mapstatus = "disqualify"

    #print(mapstatus)

    #imgurl = n.select('.beatmapset-cover')[0].get('srcset').split(',')[1][1:-3]
    time = mapnow['created_at']

    #info = n.select('.beatmapset-event__content')[0].text.replace("                ","").replace("            ","").replace("\n", "")
    info = ''
    if ('discussion' in mapnow):
        info = mapnow['discussion']['starting_post']['message']

    data = {}
    data["mapurl"] = mapurl
    data["maptitle"], data["mode"] = checkModes(mapurl)
    #data["maptitle"] = mapnow['beatmapset']['artist'] + ' - ' + mapnow['beatmapset']['title']
    #data["mode"] = 
    data["mapstatus"] = mapstatus
    #data["imgurl"] = imgurl
    data["time"] = time
    data["info"] = info
    data["hash"] = hash(time)
    print(data['maptitle'] + '(' + data['mapurl'] + ' )\n' + data['info'])
    #nominate_data.append(data)
#nominate_data.reverse()
#return nominate_data
