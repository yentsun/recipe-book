$(function(){
    $('#title').keyup(function(){
        var clone_btn = $('#clone_recipe');
        if ($(this).attr('data-title') != $(this).val()) {
            clone_btn.attr('disabled', false);
        } else {
            clone_btn.attr('disabled', true);
        }

    });
    $('#clone_recipe').click(function(){
        $(this).parents('form').attr('action', '/create_recipe').submit();
    });
    var toggle_status = $('#toggle-status');
    toggle_status.tooltip();
    if ($('[name="status_id"]').val() == 0)
        toggle_status.addClass('active');
    toggle_status.click(function(){
        var status_id_field = $('[name="status_id"]');
        status_id_field.val() == 1 ?
            status_id_field.val(0) : status_id_field.val(1);
        $.post('/update_recipe_status/'+recipe_title,
               {new_status: status_id_field.val()},
               function(data){
                   status_id_field.val(data.status_id)
               });
    });

});

function deleteRecipe(title) {
    var really_delete = confirm('Действительно удалить рецепт?');
    if (really_delete) {
        window.location = '/delete_recipe/'+title;
    } else {
        return false;
    }
}