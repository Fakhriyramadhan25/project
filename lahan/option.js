(function(window, google, mapster){

    mapster.MAP_OPTIONS = {
     center : {
         lat: 1.131231,
         lng: 104.052988
     },
//    zoom:15,
        disableDefaultUI: false,
        scrollwheel: true,
        draggable : true,
        mapTypeId: google.maps.MapTypeId.SATELLITE,
//        maxZoom: 25,
//        minZoom:3,
        zoomControlOptions : {
          position: google.maps.ControlPosition.RIGHT_TOP,
          style : google.maps.ZoomControlStyle.SMALL
      },
        panControlOption : {
            position : google.maps.ControlPosition.LEFT_BOTTOM
        },
        streetViewControlOptions: {
        position: google.maps.ControlPosition.LEFT_TOP
        }
      };

 }(window, google, window.Mapster || (window.Mapster = {})))
