Schulkarte-Leipzig
==================

Schulkarte Leipzig contains of three parts

Code
----

This section contains of 2 scripts.
schools.py is a scraper collecting names and addressses of the schools of leipzig. 
There are about 8 different categories for schools which can be fetched.
Furthermore this script uses nominatmin (OpenStreetMap-GeoLocationService) for matching 
coordinates to addresses. Attention: The error handling in this part of the script is 
in strong need of improvements. Furthermore script only works with the first result found, 
so a checking possibility for this would be nice.
converter.py converts the csv-files to geo.json files which can be used in the frontend

Daten
-----

There is data for three kinds of schools already fetched and ready to be used. 
Probably incomplete (see Error Handling in the above section for details)

Web
---

The presentation layer uses Leaflet.js to display the markers.
