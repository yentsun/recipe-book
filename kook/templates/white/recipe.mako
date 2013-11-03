<%inherit file="layout.mako"/>
<%!
    from kook.mako_filters import markdown, pretty_time
%>
<%def name="title()">
    ${recipe.dish.title} ${recipe.description}
</%def>
<%def name="js()"></%def>
<section id="recipe">
    <h1>${recipe.dish.title} <br><span>${recipe.description}</span></h1>
    <div class="row">
        <div id="photo" class="span6">
            <div>
                <img width="100%" src="${recipe.dish.image.url}" alt="">
            </div>
            <div id="photo_credit">
                Фото: ${recipe.dish.image.credit or recipe.dish.image.get_credit()}
            </div>
        </div>
        <div id="ingredients">
            <h3>Ингредиенты</h3>
            <ul>
                % for ingredient in recipe.ingredients:
                <li>${ingredient.product.title}&nbsp;&mdash;&nbsp;${ingredient.get_measured()}&nbsp;<span
                            title="${ingredient.get_unit().title}">${ingredient.get_unit().abbr}
                    </span>
                </li>
                % endfor
            </ul>
        </div>
    </div>
    <div id="steps">
            <h3>Приготовление:</h3><br>
            <table class="table" cellpadding="0" cellspacing="0">
                % for num, step in enumerate(recipe.steps, start=1):
                <tr>
                    <td class="no">
                        ${num}
                    </td>
                    <td class="text">
                        ${step.text | markdown, n}
                    </td>
                    <td>
                    % if step.time_value:
                        ${step.time_value}&nbsp;мин
                    % endif
                    </td>
                </tr>
                %endfor
            </table>
    </div>
    <div id="bottomline">
        <div id="uuid" title="идентификатор рецепта" class="pull-right">
            ${recipe.ID}
        </div>
    </div>
</section>