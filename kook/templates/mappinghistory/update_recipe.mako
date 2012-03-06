<%inherit file="layout.mako"/>
<h1><%block name="title">Редактировать рецепт</%block></h1>
% if request.session.peek_flash():
<div id="flash">
<% flash = request.session.pop_flash() %>
% for message in flash:
    ${message | n}
% endfor
</div>
% endif
<form action="${update_recipe_path}" method="post">
    <fieldset>
        <legend>Общая информация</legend>
        <p>
            <label for="title">Название</label>
            <input type="text" id="title" name="title" value="${recipe.title}" disabled>
            <input type="hidden" name="title" value="${recipe.title}">
        </p>
        <p>
            <label for="description">Описание</label>
            <textarea name="description" id="description" cols="30" rows="10">${recipe.description}</textarea>
        </p>
    </fieldset>
    <fieldset>
        <legend>Ингредиенты</legend>
        % for no, ingredient in enumerate(recipe.ingredients):
        <p class="product_amount">
            <label for="product${no}">Продукт, количество в г</label>
            <input id="product${no}" type="text" name="product" class="product_name"
                                                                value="${ingredient.product.title}">
            <input type="text" name="amount" value="${ingredient.amount}">
        </p>
        % endfor
        <button type="button" id="add_ingredient_fields">Добавить ингредиент</button>
    </fieldset>
    <fieldset>
        <legend>Приготовление</legend>
##        TODO добавить пустую форму шага, если нет шагов
        % for step in recipe.steps:
        <div class="step">
            <label for="step${step.number}">Шаг №<span>${step.number}</span></label>
            <input id="step${step.number}" type="hidden" name="step_number" value="${step.number}">
            <textarea name="step_text" id="steptext_${step.number}"
                                       cols="30" rows="10">
                ${step.text}
            </textarea>
        </div>
        % endfor
        <button type="button" id="add_step_fields">Следующий шаг</button>
    </fieldset>
    <fieldset>
        <button type="submit">Обновить рецепт</button>
    </fieldset>
</form>
<%def name="js()">
    <script type="text/javascript" src="/static/js/ckeditor/ckeditor.js"></script>
    <script type="text/javascript" src="/static/js/ckeditor/adapters/jquery.js"></script>
    <script type="text/javascript" src="/static/js/form_fields.js"></script>
    <script type="text/javascript" src="/static/js/add_recipe.js"></script>
</%def>