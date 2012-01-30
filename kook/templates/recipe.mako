<%inherit file="layout.mako"/>
<h1>Рецепт: <%block name="title">${recipe.title}</%block></h1>
<div id="text">
${recipe.description}
</div>
<div id="ingredients">
    <p>Ингредиенты:</p>
    <ul>
    % for ingredient in recipe.ingredients:
        <li>${ingredient.product.title}, ${ingredient.amount} г</li>
    % endfor
    </ul>
</div>
<div id="steps">
    <ol>
        % for phase_no, phase in recipe.phases.items():
        <li>
            % for ingredient in phase.ingredients:
            ${ingredient.product.title},
            % endfor
             ${phase.action.title}
        </li>
        % endfor
    </ol>
</div>
