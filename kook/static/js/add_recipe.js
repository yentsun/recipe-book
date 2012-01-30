$(function() {
    $('#add_ingredient_fields').click(function(){
        var duplicate = $(this).siblings('.product_amount:last').clone();
        var ingredient_no = Number(duplicate.find('.product_name').attr('data-no'));
        ingredient_no++;
        duplicate.find('input:text').val('');
        duplicate.find('.product_name').attr('data-no', ingredient_no)
        duplicate.insertBefore($(this));
    });
    $('#add_phase_fields').live('click', function(){
        var duplicate = $(this).siblings('.phase:last').clone();
        var phase_no_field = duplicate.find('input[name="phase_no"]');
        var phase_no = Number(phase_no_field.val());
        phase_no++;
        phase_no_field.val(phase_no);
        duplicate.find('label span').text(phase_no)
        duplicate.insertBefore($(this));
    });
    $('.product_name').live('blur', function(){
        var product_name = $(this).val();
        var product_no = $(this).attr('data-no');
        var ingredient_in_list = $('ul.ingredients_list li[data-no='+product_no+']');
        if (!ingredient_in_list.length) {
            $('ul.ingredients_list').append('<li data-no="'+product_no+'" class="'+product_name+'">'+product_name+'</li>');
        } else {
            $('ul.ingredients_list li[data-no='+product_no+']').text(product_name).removeClass().addClass(product_name);
        }
    });
});