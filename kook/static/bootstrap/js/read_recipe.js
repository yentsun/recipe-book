$(function(){
    $('#steps tr').click(function(){
        $(this).find('.no .btn').button('toggle');
        $(this).find('.icon-ok').toggle();
    });
});