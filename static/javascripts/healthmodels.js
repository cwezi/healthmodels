//make sure map is a global variable
var map;

function ajax_loading(element) {
    var t = $(element);
    var offset = t.offset();
    var dim = {
        left:    offset.left,
        top:    offset.top,
        width:    t.outerWidth(),
        height:    t.outerHeight()
    };
    $('<div class="ajax_loading"></div>').css({
        position:    'absolute',
        left:        dim.left + 'px',
        top:        dim.top + 'px',
        width:        dim.width + 'px',
        height:        dim.height + 'px'
    }).appendTo(document.body).show();


}

function refresh_tree() {
        ajax_loading('#tree');
        $('#tree').load('/healthfacility/render_tree/',function(){
             $('.ajax_loading').remove();
        });
      }
 function delete_facility(facility_pk) {
    	  if (confirm("Are you sure?")) {
        $.ajax({'async':false,
              'cache':false,
              'type':'POST',
              'url':'/healthfacility/' + facility_pk + '/delete/',
              'success': function() { refresh_tree(); load_add_location(); }
             });
    	  } else {
    		  return false;

    	  }
      }
 function load_edit_facility(facility_pk) {
          ajax_loading('#fac_detail');
        $('#fac_detail').load('/healthfacility/' + facility_pk + '/edit/',function(){
           $('.ajax_loading').remove();
        });
      }

function load_new_facility(parent_pk) {
          ajax_loading('#fac_detail');
        $('#fac_detail').load('/healthfacility/' + parent_pk + '/new/',function(){
           $('.ajax_loading').remove();
        });
      }

function add_facility(link) {
          form = $(link).parents("form");
          form_data = form.serializeArray();
          $('#fac_detail').load(form.attr("action"), form_data, function() { refresh_tree() });
      }

      function update_facility(link) {
          form = $(link).parents("form");
          form_data = form.serializeArray();
          $('#fac_detail').load(form.attr("action"), form_data, function() { refresh_tree() });
      }

$(document).ready(function() {
         refresh_tree();
         load_new_facility(1);

      });
