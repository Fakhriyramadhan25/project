(function(window, google, mapster){

 //map options
 var options = mapster.MAP_OPTIONS,
    element = document.getElementById('map-canvas'),
 //map
//     map = new google.maps.Map(element, options);
//google.maps.event.addListener(map.gMap, 'click', function(e){alert('click');
//console.log(e);
//});
//google.maps.event.addListener(map.gMap, 'dragend', function(e){alert('i dragged the cursor');
//});
//     map = new google.maps.Map(element, options);
//google.maps.event.addListener(map.gMap, 'click', function(e){alert('click');
//console.log(e);
//});
//google.maps.event.addListener(map.gMap, 'dragend', function(e){alert('i dragged the cursor');
//});
//     map = new google.maps.Map(element, options);
     map = mapster.create(element, options);
//    map.gMap.setZoom(16);
     map.zoom(14);

//    map._on('click',function(e){
//       alert('click');
//        console.log(e);
//        console.log(this);
//    });

    map.addMarker({
    lat:1.131231,
    lng:104.052988,
    draggable:true,
    event: {
    name:'click',
    callback: function(){
    alert('im good');
    }
    },
    });

    map.addMarker({
    lat:1.131231,
    lng:104.152988,
    draggable:true,
    event: {
    name:'dragend',
    callback: function(){
    alert('im good');
    }
    },
    });

    var marker = map.addMarker({
    lat:1.131231,
    lng:104.122988,
    draggable:true,
    content: 'good is better'
    });

//    var infoWindow = new google.maps.InfoWindow({
//        content: 'i like food'
//    });
//
//    infoWindow.open(map.gMap, marker);


    //    map.addMarker(1.131231, 104.052988,true);
//    var marker = new google.maps.Marker({
//        position: {
//            lat: 1.131231,
//            lng: 104.052988
//        },
//        map: map.gMap
//        icon: 'https://icons-for-free.com/iconfiles/png/512/location+maker+map+icon-1320166084997417306.png'
//    });

//    var marker = new google.maps.Marker({
//        position: {
//            lat: 1.131231,
//            lng: 104.112988
//        },
//        map: map.gMap
//        icon: 'https://mapicons.mapsmarker.com/wp-content/uploads/mapicons/shape-default/color-f34648/shapecolor-color/shadow-1/border-dark/symbolstyle-white/symbolshadowstyle-dark/gradient-no/welfareroom.png'
//    });

//google.maps.event.addListener(map.gMap, 'click', function(e){alert('click');
//console.log(e);
//});
//google.maps.event.addListener(map.gMap, 'dragend', function(e){alert('i dragged the cursor');
//});
    }
 (window, google, window.Mapster || (window.Mapster = {})));
