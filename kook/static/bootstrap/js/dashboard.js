$(function(){
    $('#recipe-list tr').hover(function(){
        $(this).find('.edit').toggle();
    });
});