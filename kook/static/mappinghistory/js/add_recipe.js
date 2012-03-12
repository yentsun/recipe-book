$(function() {
    $('#add_ingredient_fields').click(function(){
        var duplicate = $(this).siblings('.product_amount:last').clone();
        var ingredient_number = Number(duplicate.find('.product_name').attr('data-id'));
        ingredient_number++;
        duplicate.find('input:text').val('');
        duplicate.find('.product_name').attr('data-id', ingredient_number);
        duplicate.insertBefore($(this));
    });
    $('#add_step_fields').click(function(){
        var duplicate = $(this).siblings('.step:last').clone();
        var step_number_field = duplicate.find('input[name="step_number"]');
        var step_number = Number(step_number_field.val());
        step_number++;
        step_number_field.val(step_number);
        duplicate.find('input:text').val('');
        duplicate.find('label.step_title').text('Шаг №'+step_number);
        duplicate.find('label.step_title').attr('for', 'steptext_'+step_number);
        duplicate.find('textarea').attr('id', 'steptext_'+step_number).text('');
        duplicate.find('span').remove();
        duplicate.insertBefore($(this));
        create_ckeditor(duplicate.find('textarea'));
    });
});