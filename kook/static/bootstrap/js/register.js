$(function() {
    if (typeof error_data !== 'undefined') {
        var error_fields = error_data.errors;
        var original_data = error_data.original_data;

        //repopulate
        for (var field_name in original_data) {
            $('input[name='+field_name+']')
                .val(original_data[field_name]);
            $('textarea[name='+field_name+']')
                .text(original_data[field_name]);
        }
        // end repopulate

        //mark invalid data
        for (var field_params in error_fields) {
            var subs = field_params.split('.');
            var field_group = subs[0];
            $('.'+field_group+' label').css('color', '#B94A48')
                .append(' <span class="label label-important">'+
                error_fields[field_params]+'</span>');
        } // end mark invalid data
    }
});