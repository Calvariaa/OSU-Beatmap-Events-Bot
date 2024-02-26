import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://bn.mappersguild.com/relevantInfo"


def get_bn_status():
    response = urllib.request.urlopen(url)
    data = response.read()

    json_data = json.loads(data)

    return json_data


if __name__ == "__main__":
    print(get_bn_status())
