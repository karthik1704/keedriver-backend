(function ($) {
    $(document).on("google_point_map_widget:marker_create", function (e, lat, lng, locationInputElem, mapWrapID) {
        console.log("EVENT: marker_create"); // django widget textarea widget (hidden)
        console.log(locationInputElem); // django widget textarea widget (hidden)
        console.log(lat, lng); // created marker coordinates
        console.log(mapWrapID); // map widget wrapper element ID
    });

    $(document).on("google_point_map_widget:marker_change", function (e, lat, lng, locationInputElem, mapWrapID) {
        console.log("EVENT: marker_change"); // django widget textarea widget (hidden)
        console.log(locationInputElem); // django widget textarea widget (hidden)
        console.log(lat, lng);  // changed marker coordinates
        console.log(mapWrapID); // map widget wrapper element ID
    });

    $(document).on("google_point_map_widget:marker_delete", function (e, lat, lng, locationInputElem, mapWrapID) {
        console.log("EVENT: marker_delete"); // django widget textarea widget (hidden)
        console.log(locationInputElem); // django widget textarea widget (hidden)
        console.log(lat, lng);  // deleted marker coordinates
        console.log(mapWrapID); // map widget wrapper element ID

        if (locationInputElem === "#pickup_coordinates-mw-wrap") {
            $('#id_pickup_location').val("")
        }

        if (locationInputElem === "#drop_coordinates-mw-wrap") {
            $('#id_drop_location').val("")
        }
    })

    $(document).on("google_point_map_widget:place_changed", function (e, place, lat, lng, locationInputElem, mapWrapID) {
        console.log("EVENT: place_changed"); // django widget textarea widget (hidden)
        console.log(place);  // google geocoder place object
        console.log(locationInputElem); // django widget textarea widget (hidden)
        console.log(lat, lng); // created marker coordinates
        console.log(mapWrapID); // map widget wrapper element ID        

        if (locationInputElem === "#pickup_coordinates-mw-wrap") {
            $('#id_pickup_location').val(place.formatted_address)
        }

        if (locationInputElem === "#drop_coordinates-mw-wrap") {
            $('#id_drop_location').val(place.formatted_address)
        }

    });

    // $(function () {
    //     $("#id_pickup_area").change(() => {
    //         var cityName = $('#id_pickup_area').find(":selected").text();
    //         $("#pickup_coordinates-mw-google-address-input").val(cityName)
    //         $("#pickup_coordinates-mw-google-address-input").focus()
    //         $("#pickup_coordinates-mw-google-address-input").submit()
            
    //     })
    // })

})(jQuery)