# -*- coding: utf-8 -*-
<%page args="dish"/>
<li class="span2">
    <div class="thumbnail">
        <span class="img"
              style="background-image:url(${dish.image.url})">
        </span>
        <h3>
            <span class="title">
                ${dish.title}
            </span><br>
            <span class="description">
                рецептов: ${len(dish.recipes)}
            </span>
        </h3>
        <table class="ingredients">
            <tbody>
                % for recipe in dish.recipes:
                    <tr>
                        <td>
                            <a href="${request.route_path('read_recipe',
                            id=recipe.ID)}">
                                ${recipe.description}
                            </a>
                        </td>
                    </tr>
                % endfor
            </tbody>
        </table>
    </div>
</li>
