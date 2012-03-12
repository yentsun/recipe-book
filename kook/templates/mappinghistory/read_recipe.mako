<%inherit file="layout.mako"/>
<article>
    <h2><%block name="title">${recipe.title}</%block></h2>
    <section id="description">
        ${recipe.description | n}
    </section>
    <section id="ingredients">
        <h3>Ингредиенты:</h3>
        <ul>
            % for ingredient in recipe.ingredients:
                <li>${ingredient.product.title}, ${ingredient.amount} г</li>
            % endfor
        </ul>
    </section>
    <section id="steps">
        <h3>Приготовление:</h3>
        <table cellpadding="0" cellspacing="0">
            % for step in recipe.steps:
            <tr>
                <td>${step.number}</td>
                <td class="text">${step.text | n}</td>
                <td class="time">${step.time_value}<br><sub>мин</sub></td>
            </tr>
            %endfor
        </table>
    </section>
</article>