var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];
var grundschulen;
var oberschulen;
var gymnasien;

window.onDomReady = initReady;
window.onDomReady(initApp);

function initReady(fn)	{
	if(document.addEventListener) {
		document.addEventListener("DOMContentLoaded", fn, false);
	}
}

function initMap() {
	
	// create the tile layer with correct attribution
	var osmUrl='http://otile1.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png';

	//var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Data, imagery and map information provided by MapQuest, OpenStreetMap <http://www.openstreetmap.org/copyright> and contributors, ODbL <http://wiki.openstreetmap.org/wiki/Legal_FAQ#I_would_like_to_use_OpenStreetMap_maps._How_should_I_credit_you.#> .'
		
	//osm layer using mapquest	
	var osm = new L.TileLayer(osmUrl, {minZoom: 12, maxZoom: 18, attribution: osmAttrib});		
	//Layer containing the primary schools
	var grundsch = L.geoJson(grundschulen, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: gsIcon});
		},

		onEachFeature: onEachFeature
	});	
	
	//Layer containing the primary schools
	var obersch = L.geoJson(oberschulen, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: osIcon});
		},

		onEachFeature: onEachFeature
	});

	//Layer containing the high schools
	var gymnas = L.geoJson(gymnasien, {
		pointToLayer: function (feature, latlng) {
		return L.marker(latlng, {icon: gymIcon});
		},

		onEachFeature: onEachFeature
	});

	// set up the map
	map = new L.Map('map', {
		center: [51.335, 12.37],
	    	zoom: 14,
		layers: [osm, grundsch]	
	});

	var overlays = {
		    "Grundschulen": grundsch,
		    "Oberschulen": obersch,
		    "Gymnasien": gymnas
	};
	
	L.control.layers(overlays).addTo(map);

}

var gsIcon = L.icon({
    iconUrl: 'images/marker.png',
    shadowUrl: 'images/shadow.png',

    iconSize:     [50, 80], // size of the icon
    shadowSize:   [50, 74], // size of the shadow
    iconAnchor:   [25, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [25, 60],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var gymIcon = L.icon({
    iconUrl: 'images/marker2.png',
    shadowUrl: 'images/shadow.png',

    iconSize:     [50, 80], // size of the icon
    shadowSize:   [50, 74], // size of the shadow
    iconAnchor:   [25, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [25, 60],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

var osIcon = L.icon({
    iconUrl: 'images/marker3.png',
    shadowUrl: 'images/shadow.png',

    iconSize:     [50, 80], // size of the icon
    shadowSize:   [50, 74], // size of the shadow
    iconAnchor:   [25, 80], // point of the icon which will correspond to marker's location
    shadowAnchor: [25, 60],  // the same for the shadow
    popupAnchor:  [0, -80] // point from which the popup should open relative to the iconAnchor
});

function initApp()	{

$.getJSON( "oberschule.geo.json", function( data ) {
	oberschulen = data;
	$.getJSON( "grundschule.geo.json", function( data ) {
		grundschulen = data;
		$.getJSON( "gymnasium.geo.json", function( data ) {
			gymnasien = data;
			initMap();
		})
	})
})


}

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}
