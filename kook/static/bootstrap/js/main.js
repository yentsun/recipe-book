$(function(){
    $('input[type="text"]').each(function(){
        if ($(this).val() == 'None')
            $(this).val('');
    });
});