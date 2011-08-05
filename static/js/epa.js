// Set up namespace.
var ns = {};

ns.selectChange = function() {
  // Change the label for the select based on the
  // current question value.
  var self = $('select'),
      value = self.val(),
      paragraph = self.siblings('p'),
      label = paragraph.children('label'),
      input = paragraph.children('input');

  if (value == 'pcs') {
    label.text('Zipcode');
    input.attr('placeholder', 'Your Zipcode')
         .css('width', '');
  } else if (value == 'radinfo') {
    label.text('Location');
    input.attr('placeholder', 'Your Location')
         .css('width', '100%');
  }

};

ns.init = function() {
  // Go ahead and run the ns.selectChange function, and
  // bind ns.selectChange to the select element.
  var select = $('select'),
      selectChange = ns.selectChange;

  selectChange();
  select.change(selectChange);

};

$(ns.init);
