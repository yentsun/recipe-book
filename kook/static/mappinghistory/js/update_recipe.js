$(function(){
    $('input#title').change(function(){
        $('#clone_recipe').show();
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