$(function() {
    $('#add_ingredient_fields').click(function(){
        var container = $('#ingredients tbody');
        var duplicate = container.find('.product_amount:last').clone();
        var ingredient_number = Number(duplicate.find('.product_name').attr('data-id'));
        ingredient_number++;
        duplicate.find('input').val('');
        duplicate.find('.chosen_unit_abbr').text('г');
        duplicate.find('.alt_measures').html('');

        var product_name_input = duplicate.find('.product_name');
        product_name_input.attr('data-id', ingredient_number);
        duplicate.appendTo(container);
        product_name_input.find('input').typeahead({source:products});
        product_name_input.find('input').attr('autocomplete', 'off').focus();
    });
    $('#add_step_fields').click(function(){
        var duplicate = $(this).siblings('.step:last').clone();
        console.log(duplicate);
        var step_number_field = duplicate.find('input[name="step_number"]');
        var step_number = Number(step_number_field.val());
        step_number++;
        duplicate.find('input:text').val('');
        step_number_field.val(step_number);
        duplicate.find('textarea').attr('id', 'steptext_'+step_number).text('');
        duplicate.find('span').remove();
        duplicate.insertBefore($(this)).hide().fadeIn('slow');
        create_ckeditor(duplicate.find('textarea'));
        $(window).scrollTop(duplicate.position().top);
    });
    var product_name_inputs = $('.product_name input');
    product_name_inputs.attr('autocomplete', 'off').typeahead({source:products});
    product_name_inputs.live('change', function(){
        repopulate_measures($(this));
    });
    $('.remove').live('click', function(){
        $(this).parents('.removable').fadeOut('slow', function(){
            $(this).remove();
        });
    });
});

function set_measure(cont, apu_unit_title, apu_unit_abbr, apu_amount) {
    cont = $(cont);
    var top_parent = cont.parents('.amount');
    top_parent.find('input[name=measured_amount]').attr('data-multiplier', apu_amount).keyup();
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
        if (data.length > 0) {
            var items = [];
            $.each(data, function(key, item) {
                items.push(' <li><a onclick="set_measure(this, \''+item.title+'\',\''+item.abbr+'\', '+item.amount+')">'+item.title+'</a></li>');
            });
            var parent = cont.parents('.product_amount');
            parent.find('[name=measured_amount]').val('');
            parent.find('[name=amount]').val('0');
            parent.find('.chosen_unit_abbr').text('г ');
            parent.find('.alt_measures').html('<li class="divider"></li>'+items.join(''));
        }
    });
}