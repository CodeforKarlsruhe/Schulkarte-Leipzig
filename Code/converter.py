#!/usr/bin/env python2

import csv
from geojson import Feature, Point, FeatureCollection, dumps

schools = []

with open('oberschulen.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for element in reader:
        text = '<b>' + element[0] + '</b><br />' + element[1].lstrip()
        school = Feature(
                geometry=Point(
                    (float(element[3].lstrip()),
                    float(element[2].lstrip()))),
                properties={
                    "name": element[0],
                    "popupContent" : text
                    })
        schools.append(school)

print FeatureCollection(schools)
