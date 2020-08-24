(function(window, google, mapster){

 //map options
 var options = mapster.MAP_OPTIONS,
    element = document.getElementById('map-canvas'),
 //map
     map = new google.maps.Map(element, options);
google.maps.event.addListener(map.gMap, 'click', function(e){alert('click');
console.log(e);
});
google.maps.event.addListener(map.gMap, 'dragend', function(e){alert('i dragged the cursor');
});
    }
 (window, google, window.Mapster || (window.Mapster = {})));
