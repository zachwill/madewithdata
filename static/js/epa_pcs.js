// Set up a namespace.
var ns = {};

ns.buildingData = function(event) {
    // When hovering or having clicked a `.building` link,
    // the data should be displayed in the `float_left` div.
    var self = $(this),
        text = self.text(),
        div = self.closest('div').siblings('.float_left'),
        toggle = div.data('toggle'),
        eventData = div.data('eventData');

    if (text && !toggle) {
        div.css('background', '#333').data({
            toggle: true,
            eventData: event.type
        });
        console.log(div.data());
    } else if (event.type == 'click' && eventData == 'mouseenter' && toggle) {
        // We don't need to do anything in this instance. The user
        // hovered and then clicked the name of the business.
    } else {
        div.css('background', '')
           .data('toggle', false);
    }
}

ns.init = function() {
    var building = $('.building');
    building.live('click hover', ns.buildingData);
}

$(ns.init);
