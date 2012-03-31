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
});

function deleteRecipe(title) {
    var really_delete = confirm('Действительно удалить рецепт?');
    if (really_delete) {
        window.location = '/delete_recipe/'+title;
    } else {
        return false;
    }
}