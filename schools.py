#!/usr/bin/env python2

import scraperwiki
import lxml.html
import sys
from lxml import etree

#DEBUG
debug = 0

#Select school type from list below
school_type = 2

#User-Agent
user_agent = "CodeForGermany, OK-Lab Leipzig, Schoolscraper"
params = ""

#List containing URLs to lists of schools in Leipzig
# 0 - Gymnasien
# 1 - Oberschulen
# 2 - Grundschulen
# 3 - Gemeinschaftsschulen
# 4 - Foerderschulen
# 5 - Berufliche Schulen
# 6 - Freie Traegerschaft
# 7 - Zweiter Bildungsweg
urls = [
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/gymnasien/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898",
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/oberschulen/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898",
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/grundschulen/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898",
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/gemeinschaftsschule/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898",
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/foerderschulen/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898",
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/berufliche-schulen/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898",
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/schulen-in-freier-traegerschaft/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898",
        "http://www.leipzig.de/jugend-familie-und-soziales/schulen-und-bildung/schulen/zweiter-bildungsweg/?tx_ewerkaddressdatabase_pi[showAll]=1&tx_ewerkaddressdatabase_pi[query]=&tx_ewerkaddressdatabase_pi[action]=teaser&tx_ewerkaddressdatabase_pi[controller]=Address&cHash=a93d7d3d290196a5cae69c80e6190898"
        ]

#Nominatim URL - to get a coordinate to an address
nom_url_1 = "http://nominatim.openstreetmap.org/search?q="
nom_url_2 = "&format=xml&polygon_kml=0&countrycodes=de&addressdetails=0"

# Result List containing the addresses
# sould contain a list with name, address, lat, lon
result = []

if debug == 1:
    print "Fetching Data"

school_html = scraperwiki.scrape(urls[school_type],params,user_agent)
school_root = lxml.html.fromstring(school_html)

if debug == 1:
    print "Parsing Response"

for school in school_root.cssselect('div[class="address-list-item address-list-item-teaser clearfix"]'):

    #Extracting the school name
    name = school.cssselect("a")
    name = name[0].text_content().encode("UTF-8")
    name = name.split("-", 1)

    address = school.cssselect("li")

    # Exception for Gymnasium Engelsdorf
    if len(address) == 3:
        address = address[1].text_content().encode("UTF-8")
    else:
        address = address[0].text_content().encode("UTF-8")

    #Extracting the Address
    address = address.split("(")[0]         # removes the Ortsteil-Part
    address_human = " ".join(address.split())
    address = "%20".join(address.split())

    #Matching Coordinates
    root_osm = etree.fromstring(scraperwiki.scrape(nom_url_1 + address + nom_url_2))
    try:
        child = root_osm[0]
    except:
        print "Error"
        continue
    lat = child.get('lat')
    lon = child.get('lon')

    if len(name) == 2:
        name = name[1].strip()
    elif len(name) == 1:
        name = name[0]
    else:
        print "Error"

    data = {
            'name' : unicode(name, errors='replace'),
            'address' : unicode(address_human, errors='replace'),
            'lat' : unicode(lat),
            'lon' : unicode(lon)
        }

    result.append(data)

    print "%s; %s; %s; %s" % (name, address_human, lat, lon)


if debug == 1:
    print "Saving Database"

scraperwiki.sqlite.save(unique_keys=['name'], data=result)
