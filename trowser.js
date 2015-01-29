gmaps = {
 
    map: null,
    clique: null,

    // google markers objects
    markers: {},
 
    // google lat lng objects
    latLngs: [],
 
    // our formatted marker data objects
    googleMarker: {},

    eGoogleMarker: {},

    // google markers objects
    emarkers: {},
 
    // google lat lng objects
    elatLngs: [],
 
    // our formatted marker data objects
    emarkerData: [],

    scale: .1,
    // add a marker given our formatted marker data object
    addMarker: function(marker) {
        var gLatLng = new google.maps.LatLng(marker.lat, marker.lng);
        var gMarker = new google.maps.Marker({
            position: gLatLng,
            map: this.map,
            title: marker.title,
            // animation: google.maps.Animation.DROP,
            icon:'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
        });
        this.latLngs.push(gLatLng);
        this.markers.push(gMarker);
        //this.markerData.push(marker);
        return gMarker;
    },

    addLine: function(line) {
	var l = new google.maps.Polyline({
	    path: [new google.maps.LatLng(line.v1_lat, line.v1_lon), new google.maps.LatLng(line.v2_lat, line.v2_lon)],
	    geodesic: true,
	    strokeColor: '#FF0000',
	    strokeOpacity: .7,
	    strokeWeight: .1
	});

        this.emarkers[line._id] = l;
        this.addToMarker(this.googleMarker, line.size, l);
	this.addToMarker(this.eGoogleMarker, line.width, l);
	l.setMap (this.map);

        return l;
    },

    addOval: function(c) {

        // solves the quadratic formula for the eigenvectors of the covariance matrix, where we solve for eigenvectors 
	// of the form [v 1] and then normalize them.
	var sr = Math.sqrt ((c.cov_tt - c.cov_nn)*(c.cov_tt - c.cov_nn) + 4 * c.cov_tn * c.cov_tn)/(2 * c.cov_tn);
	var a = (c.cov_nn - c.cov_tt) / (2 * c.cov_tn);

	// the eigenvectors of the covariance matrix
	var v1 = a + sr;
	var v2 = a - sr;

	var ev1 = c.cov_tn * v1 + c.cov_tt;
	var ev2 = c.cov_tn * v2 + c.cov_tt;

	var phi = Math.atan(v1);
	var ea = Math.sqrt(ev1);
	var eb = Math.sqrt(ev2);

	var points = [];

	var first;
	for (var theta = 0.0; theta <= 2 * Math.PI; theta += Math.PI/24) {
	    var r = ea * eb / Math.sqrt(eb * Math.cos(theta) * eb * Math.cos(theta) + ea * Math.sin(theta) * ea * Math.sin(theta));
	    points.push(new google.maps.LatLng (this.scale * r * Math.sin(theta + phi + Math.PI/2) + c.mean_lat, this.scale * r * Math.cos(theta + phi + Math.PI/2) + c.mean_lon));
	    
	}
/*	for (t = 0.0; t < 2 * Math.PI; t += Math.PI/24) {
	    var lat = (ev1 * Math.cos(t)) * (1/norm1) - (ev2 * Math.sin(t)) * (v1/norm1) + c.mean_lat;
	    if (t == 0.0) first = new google.maps.LatLng ((ev1 * Math.cos(t)) * (1/norm1) - (ev2 * Math.sin(t)) * (v1/norm1) + c.mean_lat, 
						(ev1 * Math.cos(t)) * (v1/norm1) + (ev2 * Math.sin(t)) * (1/norm1) + c.mean_lon);
	    points.push(new google.maps.LatLng ((ev1 * Math.cos(t)) * (1/norm1) - (ev2 * Math.sin(t)) * (v1/norm1) + c.mean_lat, 
						(ev1 * Math.cos(t)) * (v1/norm1) + (ev2 * Math.sin(t)) * (1/norm1) + c.mean_lon));
	}
	points.push.first;
*/
	var gMarker = new google.maps.Polygon({
	    paths: points,
	    strokeColor: '#FF0000',
	    strokeOpacity: 0.5,
	    strokeWeight: 0.01,
	    fillColor: '#FF0000',
	    fillOpacity: 0.5
	});
	var center = new google.maps.Circle({
	    strokeColor: '#440000',
	    strokeOpacity: 1,
	    strokeWeight: 0,
	    fillColor: '#000000',
	    fillOpacity: 1,
	    //map: this.map,
	    center: new google.maps.LatLng(c.mean_lat, c.mean_lon),
	    radius: 100
	});
	this.latLngs.push(points);
        this.markers[c.id] = [gMarker, center];
        this.addToMarker(this.googleMarker, c.size, center);
        this.addToMarker(this.googleMarker, c.size, gMarker);

	google.maps.event.addListener(gMarker, 'click', function() {
	    Session.set('itemsLimit', 20);
	    Session.set('clique', c.clique);
	    console.log(c.clique);
	});

	gMarker.setMap (this.map);
	center.setMap (this.map);
	return gMarker;
    },


    // check if a marker already exists
    markerExists: function(key) {
	return key in this.markers;
    },

    // check if a marker already exists
    emarkerExists: function(key) {
        return key in this.emarkers;
    },

    clearMarkers: function (marker, from, to) {
	for (var j = from; j < to; j++) {
	    console.log ("j = " + j);
	    if (j in marker) {
		for (var i = 0; i < marker[j].length; i++) {
		    marker[j][i].setMap(null);
		    console.log("marker set null");
		}
	    }
	}
    },

    addToMarker: function (marker, key, v) {
	if (!(key in marker)) {
	    marker[key] = [];
	}
	marker[key].push(v);
	//console.log("adding to marker");
    },

    // initialize the map
    initialize: function() {
        console.log("[+] Intializing Google Maps...");
        var mapOptions = {
            zoom: 12,
            center: new google.maps.LatLng(43.141078,-77.618408),
            mapTypeId: google.maps.MapTypeId.TERRAIN
        };
 
        this.map = new google.maps.Map(
            document.getElementById('map-canvas'),
            mapOptions
        );
 
        // global flag saying we intialized already
        Session.set('map', true);
	
    }
}

if (Meteor.isClient) {
  // counter starts at 0
  var ITEMS_INCREMENT = 20;
  Session.setDefault('itemsLimit', ITEMS_INCREMENT);
  Session.setDefault('clique', []);
  Session.setDefault("counter", 0);
  Session.setDefault("min_clique", 11);
  Session.setDefault("min_width", 4);
  Session.setDefault("min_clique_last", 0);
  Session.setDefault("min_width_last", 0);

  Twitter = new Mongo.Collection("twitter");
  Cliques = new Mongo.Collection("cliques");
  Edges = new Mongo.Collection("edges");

  Template.tweets.rendered = function () {
      Deps.autorun(function () {
        Meteor.subscribe('twitter',  Session.get('itemsLimit'), Session.get('clique'));
      });
  }

  
  Template.map.rendered = function() {
    if (! Session.get('map'))
        gmaps.initialize();
 
      Deps.autorun(function() {

	  var clique_sub = Meteor.subscribe('cliques', Session.get('min_clique'));
	  var edge_sub = Meteor.subscribe('edges', Session.get('min_clique'), Session.get('min_width') );

          cs = Cliques.find({tweets: { $gt: 0 }, size: {$gt: Session.get('min_clique')}}).fetch();
	 // console.log(Session.get("min_clique") + " vs " + Session.get("min_clique_last"));
	  if (Session.get("min_clique") != Session.get("min_clique_last")) {
	      console.log("clearing markers");
	      gmaps.clearMarkers(gmaps.googleMarker,  Session.get("min_clique_last"), Session.get("min_clique")); 
	      Session.set("min_clique_last", Session.get("min_clique"));
	  }
	  
	  console.log ("Min size: " +  Session.get('min_clique'));
	  console.log ("Query size: " + cs.length);
	  _.each(cs, function(c) {
	      
	      // check if marker already exists
	      if (!gmaps.markerExists(c.id)) {
		  //gmaps.addMarker(objMarker);
		  gmaps.addOval(c);
	      }
	      else {
		  gmaps.markers[c.id][0].setMap(gmaps.map);
		  gmaps.markers[c.id][1].setMap(gmaps.map);
	      }
	  });
	  
          es = Edges.find({size: { $gt : Session.get("min_clique")}, width: {$gt : Session.get("min_width")}}).fetch();
	  if (Session.get("min_width") != Session.get("min_width_last")) {
	      gmaps.clearMarkers(gmaps.eGoogleMarker, Session.get("min_width_last"), Session.get("min_width")); 
	      Session.set("min_width_last", Session.get("min_width"));
	  }
	  
          _.each(es, function(e) {
	      
	      // check if marker already exists
	      if (!gmaps.emarkerExists(e._id)) {
		  gmaps.addLine(e);
	      }
	      else {
		  gmaps.emarkers[e._id].setMap(gmaps.map);
	      }
	  });
      });
      
  }
    
  Template.map.destroyed = function() {
    Session.set('map', false);
  }

 

  Template.map_filter.helpers ({
      min_clique: function () {
	 return Session.get("min_clique");
      },
      min_width: function () {
	 return Session.get("min_width");
      }
  });

  Template.tweets.twitter = function () {
     // return Twitter.find();
    var clique = Session.get("min_clique");
   
   if (clique.length > 0) {
	    return Twitter.find({players : {$in: clique}, num_players : {$gt: 1}}, {sort: {time_s:1}, limit:limit});
	    //return Twitter.find({screen_name : {$in: clique}}, {sort: {time_s:1}, limit:Session.get("itemsLimit")});
    }
    else return Twitter.find({}, {sort: {time_s:1}, limit:Session.get("itemsLimit")});
  }

  Template.tweets_info.names = function () {
      return Session.get("clique").join(", ");
     
  }
  Template.tweets.moreResults = function() {
      console.log("Items Count: " +Session.get("itemsLimit"));
      console.log("Items Count: " + Template.tweets.twitter().count());
      return !(Template.tweets.twitter().count() < Session.get("itemsLimit"));
  }

  Template.tweets.one = function () {
      // return Twitter.findOne();
  }

  Template.map_filter.events({
    'blur .cliques': function (b, template) {
	var min_width =  parseInt(template.find("#min_width").value)
	var min_clique = parseInt(template.find("#min_clique").value)
	min_clique =  Math.max(min_clique, min_width+1);
	min_width = Math.min(min_width, min_clique-1);
	//if (min_clique != Session.get("min_clique") && max_clique != Session.get("max_clique"))
	    //gmaps.clearMarkers();
	//console.log (min_clique + " " + min_clique_last);
	Session.set("min_clique", min_clique);
	console.log("Blah");
	Session.set("min_width", min_width);

    }
  });

  function showMoreVisible() {
    
   var threshold, target = $("#showMoreResults");
    if (!target.length) return;
    

    threshold = $(window).scrollTop() + $(window).height() - target.height();
 
    if (target.offset().top < threshold) {
        if (!target.data("visible")) {
            console.log("target became visible (inside viewable area)");
            target.data("visible", true);
            Session.set("itemsLimit",
                Session.get("itemsLimit") + ITEMS_INCREMENT);
        }
    } else {
        if (target.data("visible")) {
            console.log("target became invisible (below viewable area)");
            target.data("visible", false);
        }
    }        
  }
  $(window).scroll(showMoreVisible);
 // google.maps.event.addDomListener(window, 'load', initialize);
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup
      Twitter = new Mongo.Collection('twitter');
      Cliques = new Mongo.Collection('cliques');
      Edges = new Mongo.Collection('edges');

     Meteor.publish("twitter", function(limit, clique) {
	if (clique.length > 0) {
	    //return Twitter.find({players : {$in: clique}}, {sort: {time_s:1}, limit:limit});
	    return Twitter.find({players : {$in: clique}, num_players : {$gt: 1}}, {sort: {time_s:1}, limit:limit});
	}
	else
	      return Twitter.find({}, {limit:limit});
     });

      Meteor.publish("cliques", function(min_clique) {
	//  console.log("BOOGEY");
	  console.log(min_clique)
	  return Cliques.find({tweets: { $gt: 0 }, size: {$gt: min_clique}});
      });

      Meteor.publish("edges", function(min_clique, min_width) {
	  return Edges.find({size: { $gt : min_clique}, width: {$gt : min_width}});
	
	
      });
  });
}
