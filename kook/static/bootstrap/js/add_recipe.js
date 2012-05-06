$(function() {
    var ingredient_container = $('#ingredients tbody');
    var step_container = $('#steps');
    $('#add_ingredient_fields').click(function(){
        clone_ingredient(ingredient_container);
    });
    $('#add_step_fields').click(function(){
       clone_step(step_container);
    });
    var product_name_inputs = $('.product_title input');
    product_name_inputs.attr('autocomplete', 'off')
        .typeahead({source:products});
    product_name_inputs.live('change', function(){
        repopulate_measures($(this));
    });
    $('.remove').live('click', function(){
        $(this).parents('.removable').fadeOut('slow', function(){
            $(this).remove();
        });
    });
    if (typeof error_data !== 'undefined') {
        var error_fields = error_data;

        //mark invalid data
        for (var field_params in error_fields) {
            var subs = field_params.split('.');
            var field_group = subs[0];
            var element_field_name = subs[2];
            var element_no = parseInt(subs[1]);
            if (field_group && element_field_name == undefined) {
                $('.'+field_group+' label').css('color', '#B94A48')
                    .append(' <span class="label label-important">'+
                    error_fields[field_params]+'</span>');
            } else {
                if (element_field_name == 'amount')
                    element_field_name = 'measured_amount';
                if (element_field_name == 'text')
                    element_field_name = 'step_text';
                $('.'+field_group+' .removable').eq(element_no)
                    .find('[name='+element_field_name+']')
                    .css('background', '#F2DEDE')
                    .attr('data-original-title',
                          error_fields[field_params])
                    .tooltip({placement:'top'});
            }
        } // end mark invalid data
    }
    $('#tags').chosen();
    $('textarea').markItUp(mySettings);
});

function set_measure(cont, apu_unit_title, apu_unit_abbr, apu_amount) {
    cont = $(cont);
    var top_parent = cont.parents('.amount');
    top_parent.find('input[name=measured_amount]')
        .attr('data-multiplier', apu_amount).keyup();
    top_parent.find('.chosen_unit_abbr').text(apu_unit_abbr);
    top_parent.find('input[name=unit_title]').val(apu_unit_title);
}

function set_amount(cont) {
    cont = $(cont);
    var parent = cont.parents('.amount');
    var current_value = cont.val();
    var multiplier = cont.attr('data-multiplier');
    if (multiplier != undefined) {
        var new_amount = current_value * multiplier;
    } else
        var new_amount = current_value;
    parent.find('[name=amount]').val(new_amount);
}

function repopulate_measures(cont) {
    $.getJSON('/product_units/'+cont.val(), function(data){
        var parent = cont.parents('.product_amount');
        parent.find('.chosen_unit_abbr').text('г ');
        if (data.length > 0) {
            var items = [];
            $.each(data, function(key, item) {
                items.push(' <li><a onclick="set_measure(this, \''+
                    item.title+'\',\''+
                    item.abbr+'\', '+
                    item.amount+')">'+
                    item.title+'</a></li>');
            });
            parent.find('.alt_measures')
                .html('<li class="divider"></li>'+items.join(''));
        } else {
            parent.find('.alt_measures').html('');
        }
    });
}

function clone_ingredient(container, data) {
    var original = container.find('.product_amount:last');
    var duplicate = original.clone();
    duplicate.find('input').val('').css('background', '#fff');
    duplicate.find('.chosen_unit_abbr').text('г');
    duplicate.find('.alt_measures').html('');
    duplicate.appendTo(container);
    var product_title_input = duplicate.find('[name=product_title]');
    product_title_input.typeahead({source:products});
    product_title_input.attr('autocomplete', 'off').focus();
    if (data != undefined) {
        product_title_input.val(data.product_title);
        repopulate_measures(product_title_input);
        duplicate.find('[name="amount"]').val(data.amount);
        duplicate.find('[name="measured_amount"]').val(data.amount);
        if (original.find('[name="product_title"]').val() == '')
            original.remove();
    }
}

function clone_step(container, data) {
    var original = container.find('.step:last');
    var duplicate = original.clone();
    duplicate.remove();
    var step_number_field =
        duplicate.find('input[name="step_number"]');
    var step_number = Number(step_number_field.val());
    step_number++;
    duplicate.find('input:text').val('');
    step_number_field.val(step_number);
    duplicate.attr('id', 'step_'+step_number);
    duplicate.find('textarea').text('').css('background', '#fff');
    duplicate.appendTo(container);
    $(window).scrollTop(duplicate.position().top);
    if (data != undefined) {
        step_number_field.val(data.number);
        duplicate.find('[name=time_value]').val(data.time_value);
        duplicate.find('[name=step_text]').text(data.text);
        if (original.find('textarea').text() == '') {
            original.remove();
        }
    }
    duplicate.find('textarea').markItUp(mySettings);
}

function name_with_value_exists(name, value) {
    return $('[name="'+name+'"][value="'+value+'"]').length;
}