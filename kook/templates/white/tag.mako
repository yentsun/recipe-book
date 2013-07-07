<%inherit file="layout.mako"/>
<%def name="title()">${tag.title}</%def>
<%def name="js()"></%def>
<section id="tag">
    <hr>
    <h2>${tag.title}</h2>
    <ul class="thumbnails">
    % for dish in dishes:
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
                        <img width="16" height="16"
                             src="${recipe.author.gravatar_url()}">
                    </td>
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
    % endfor
    </ul>
</section>