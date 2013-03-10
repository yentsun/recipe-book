from kook.models import recipe
from beaker.cache import cache_region, region_invalidate


@cache_region('long_term')
def get_bundle():
    """Return bundle dict with `Products`, `Dishes` and `Tags`"""
    return {'products': recipe.Product.fetch_all(),
            'dishes': recipe.Dish.fetch_all(),
            'tags': recipe.Tag.fetch_all()}


@cache_region('long_term')
def get_recipe(id_):
    """Return recipe by id"""
    return recipe.Recipe.fetch(id_)


def clear_recipe(id_):
    """Clear all caches for a recipe"""
    region_invalidate(get_recipe, 'long_term', id_)
    region_invalidate(get_bundle, 'long_term')
