# -*- coding: utf-8 -*-
<%page args="recipe"/>
<li class="span2">
    <div class="thumbnail">
        <a class="img" href="${request.route_path('read_recipe', id=recipe.ID)}"
                %if recipe.dish.image:
                  style="background-image:url(${recipe.dish.image.url})"
                %endif
            title="${recipe.dish.title} ${recipe.description}">
        </a>
        <h3>
            <a href="${request.route_path('read_recipe', id=recipe.ID)}"
               title="${recipe.dish.title} ${recipe.description}">
            <span class="title">
                ${recipe.dish.title}
            </span><br>
            <span class="description">
                ${recipe.description}
            </span>
            </a>
        </h3>
        <table class="ingredients">
            <tbody>
                %for ingredient in recipe.ingredients:
                <tr>
                    <td>${ingredient.product.title}</td>
                    <td>${ingredient.get_measured()}&nbsp;${ingredient.get_unit().abbr}
                    </td>
                %endfor
            </tr>
            </tbody>
        </table>
    </div>
</li>