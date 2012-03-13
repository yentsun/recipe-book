function deleteRecipe(title) {
    var really_delete = confirm('Действительно удалить рецепт?');
    if (really_delete) {
        window.location = '/delete_recipe/'+title;
    } else {
        return false;
    }
}