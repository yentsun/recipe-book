from kook.models import recipe
from kook.models import user
from beaker.cache import cache_region, region_invalidate


@cache_region('long_term')
def get_recipe_bundle():
    """Return cached bundle dict with `Products`, `Dishes` and `Tags`"""
    return {'products': recipe.Product.fetch_all(),
            'dishes': recipe.Dish.fetch_all(),
            'tags': recipe.Tag.fetch_all()}


@cache_region('long_term')
def get_recipe(recipe_id):
    """Return cached recipe by id"""
    return recipe.Recipe.fetch(recipe_id)


def clear_recipe(recipe_id):
    """Clear all caches for a recipe"""
    region_invalidate(get_recipe, 'long_term', recipe_id)
    region_invalidate(get_recipe_bundle, 'long_term')


@cache_region('long_term')
def get_user(user_id):
    """Return cached user by id"""
    return user.User.fetch(user_id)


@cache_region('long_term')
def clear_user(user_id):
    """Clear user caches"""
    region_invalidate(get_user, 'long_term', user_id)