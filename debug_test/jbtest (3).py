from bs4 import BeautifulSoup
import urllib.request
import json
import socket
socket.setdefaulttimeout(60)

url = "https://osu.ppy.sh/beatmapsets/events?types%5B%5D=nominate&types%5B%5D=qualify&types%5B%5D=rank&types%5B%5D=love&types%5B%5D=nomination_reset&types%5B%5D=disqualify"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
jschecker = (soup.find(id="json-users")).string.lstrip()

#print(type(jshtml))
#print (jshtml)
mapjson = json.loads(jshtml)
#print(mapjson)


for mapchecker in mapjson:
    print(mapchecker['username'])
