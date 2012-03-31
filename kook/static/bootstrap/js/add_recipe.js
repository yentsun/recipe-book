$(function() {
    $('#add_ingredient_fields').click(function(){
        var container = $('#ingredients tbody');
        var duplicate = container.find('.product_amount:last').clone();
        var ingredient_number = Number(duplicate.find('.product_name').attr('data-id'));
        ingredient_number++;
        duplicate.find('input:text').val('');
        var product_name_input = duplicate.find('.product_name');
        product_name_input.attr('data-id', ingredient_number);
        duplicate.appendTo(container);
        product_name_input.find('input').typeahead({source:products});
        product_name_input.find('input').attr('autocomplete', 'off').focus();
    });
    $('#add_step_fields').click(function(){
        var duplicate = $(this).siblings('.step:last').clone();
        var step_number_field = duplicate.find('input[name="step_number"]');
        var step_number = Number(step_number_field.val());
        step_number++;
        duplicate.find('input:text').val('');
        step_number_field.val(step_number);
        duplicate.find('label.step_title').attr('for', 'steptext_'+step_number);
        duplicate.find('textarea').attr('id', 'steptext_'+step_number).text('');
        duplicate.find('span').remove();
        duplicate.insertBefore($(this));
        create_ckeditor(duplicate.find('textarea'));
    });
    $('.product_name input').attr('autocomplete', 'off').typeahead({source:products});
    $('.remove').live('click', function(){
        $(this).parents('.removable').fadeOut('slow', function(){
            $(this).remove();
        });
    });
});