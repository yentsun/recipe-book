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
        % for step in recipe.steps:
        <li>
             ${step.text | n}
        </li>
        % endfor
    </ol>
</div>
