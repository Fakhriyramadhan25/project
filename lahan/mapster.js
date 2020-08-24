(function(window, google){
    var Mapster = (function(){
        function Mapster (element, opts){
        this.gMap = new google.maps.Map(element,opts);

    }
    Mapster.prototype = {

    };
        return Mapster;
       }());
 Mapster.create = function(){
     return new Mapster(element, opts);
 };
    window.Mapster = Mapster;
}
(window, google))
