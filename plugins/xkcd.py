import re

import requests
from bs4 import BeautifulSoup

from cloudbot import hook

xkcd_re = re.compile(r'(.*:)//(www.xkcd.com|xkcd.com)(.*)', re.I)
months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
          9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def xkcd_info(xkcd_id, url=False):
    """ takes an XKCD entry ID and returns a formatted string """
    request = requests.get("http://www.xkcd.com/" + xkcd_id + "/info.0.json")
    request.raise_for_status()
    data = request.json()
    date = "{} {} {}".format(data['day'], months[int(data['month'])], data['year'])
    if url:
        url = " | http://xkcd.com/" + xkcd_id.replace("/", "")
    return "xkcd: \x02{}\x02 ({}){}".format(data['title'], date, url if url else "")


def xkcd_search(term):
    search_term = requests.utils.quote(term)
    url_base = "http://www.ohnorobot.com/index.php?comic=56&s={}"
    request = requests.get(url_base.format(search_term))
    request.raise_for_status()
    soup = BeautifulSoup(request.text)
    result = soup.find('li')
    if result:
        url = result.find('div', {'class': 'tinylink'}).text
        xkcd_id = url[:-1].split("/")[-1]
        print(xkcd_id)
        return xkcd_info(xkcd_id, url=True)
    else:
        return "No results found!"


@hook.regex(xkcd_re)
def xkcd_url(match):
    xkcd_id = match.group(3).split(" ")[0].split("/")[1]
    return xkcd_info(xkcd_id)


@hook.command()
def xkcd(text):
    """<search term> - Search for xkcd comic matching <search term>"""
    return xkcd_search(text)
