import requests
import argparse
from lxml import html


def get_me_stuf(page):
    tree = html.fromstring(page.text)
    dates = tree.xpath("//table[@class='results']/tbody/tr[1]/td[2]/text()")
    departures = tree.xpath("//table[@class='results']/tbody/tr[1]/td[5]/text()")
    stations = tree.xpath("//table[@class='results']/tbody/tr[1]/td[3]/text()")
    vehicles = tree.xpath("//table[@class='results']/tbody/tr[1]/td[7]/img[1]/@title")

    end_station = tree.xpath("//table[@class='results']/tbody/tr[position() = (last()-1)]/td[3]/text()")
    arrivals = tree.xpath("//table[@class='results']/tbody/tr[position() = (last()-1)]/td[4]/text()")

    #arrivals = tree.xpath("//table[@class='results']/tbody/tr/td[starts-with(@class, 'suppress']/text()")
    #departures = tree.xpath("//table[@class='results']/tbody/tr/td[starts-with(@class, 'suppress']/following-sibling/text()")
    return dates, departures, stations, vehicles, arrivals, end_station



parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-f','--dfrom', help='Destination from', required=True)
parser.add_argument('-t','--dto', help='Destination to', required=True)
args = parser.parse_args()

d_from = args.dfrom
d_to = args.dto


session = requests.Session()

tokenRequest = session.get('https://cp.hnonline.sk/vlakbusmhd/spojenie/')
tree = html.fromstring(tokenRequest.text)
#headers = tokenRequest.headers

elements = tree.xpath("//*[starts-with(@id, '__')]/@id")
vals = tree.xpath("//*[starts-with(@id, '__')]/@value")
dictionary = dict(zip(elements, vals))


some_stuff = {'ctl00$cDM$cF$0t': d_from,
           'ctl00$cDM$cF$0h': d_from,
           'ctl00$cDM$cT$0t': d_to,
           'ctl00$cDM$cT$0h': d_to,
           'IsDepTime': 'true',
           'ctl00$cDM$cSB$cmdSearch': "Hľadať"}

payload = {**some_stuff, ** dictionary}

res = session.post('https://cp.hnonline.sk/vlakbusmhd/spojenie/', data=payload)


print(get_me_stuf(res))


#print(res.text)
