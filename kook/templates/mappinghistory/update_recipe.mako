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
<form class="common" action="${update_recipe_path}" method="post">
    <fieldset>
        <legend></legend>
        <p>
            <label for="title">Название</label>
            <input type="text" id="title" name="title" value="${recipe.title}">
        </p>
        <p>
            <label for="description">Описание</label>
            <textarea name="description" id="description" cols="30" rows="10">${recipe.description}</textarea>
        </p>
    </fieldset>
    <fieldset>
        <legend>Ингредиенты</legend>
        % for no, ingredient in enumerate(recipe.ingredients):
        <section class="product_amount">
            <p class="product_name">
                <label for="product${no}">Продукт</label>
                <input id="product${no}" type="text" name="product"
                       data-id="${no}" value="${ingredient.product.title}">
            </p>
            <p class="amount">
                <label for="amount${no}">количество, г</label>
                <input id="amount${no}" type="text" name="amount"
                       value="${ingredient.amount}">
            </p>
        </section>
        % endfor
        <button type="button" class="button add" id="add_ingredient_fields">
            еще ингредиент
        </button>
    </fieldset>
    <fieldset>
        <legend>Приготовление</legend>
##        TODO добавить пустую форму шага, если нет шагов
        % for step in recipe.steps:
        <section class="step">
            <label class="step_title"
                   for="steptext_${step.number}">Шаг №<span>${step.number}</span></label>
            <input id="step${step.number}" type="hidden" name="step_number"
                   value="${step.number}">
            <textarea name="step_text" id="steptext_${step.number}"
                                       cols="30" rows="10">
                ${step.text}
            </textarea>
            <p class="time_value">
                <label for="timevalue_${step.number}">время, мин</label>
                <input type="text" name="time_value"
                       id="timevalue_${step.number}" value="${step.time_value}">
            </p>
            <p class="note">
                <label for="note_${step.number}">Примечание</label>
                <input type="text" name="note" id="note_${step.number}"
                        value="${step.note}">
            </p>
        </section>
        % endfor
        <button type="button" class="button add" id="add_step_fields">Следующий шаг</button>
    </fieldset>
    <fieldset class="final_action">
        <button type="submit" class="button submit"
                id="submit_recipe">Обновить рецепт</button>
        <button type="button" class="button delete"
                id="delete_recipe" onclick="deleteRecipe('${recipe.title}');">Удалить рецепт</button>
    </fieldset>
</form>
<%def name="css()">
    <link rel="stylesheet" href="/static/flash-messages/main.css"
          type="text/css" media="screen" />
</%def>
<%def name="js()">
    <script type="text/javascript"
            src="/static/mappinghistory/js/ckeditor/ckeditor.js"></script>
    <script type="text/javascript"
            src="/static/mappinghistory/js/ckeditor/adapters/jquery.js"></script>
    <script type="text/javascript"
            src="/static/mappinghistory/js/jquery-ui-1.8.18.custom.min.js"></script>
    <script type="text/javascript" src="/static/mappinghistory/js/form_fields.js"></script>
    <script type="text/javascript" src="/static/mappinghistory/js/add_recipe.js"></script>
    <script type="text/javascript" src="/static/mappinghistory/js/update_recipe.js"></script>
</%def>
<script type="text/javascript">
    var products = [
        % for product in products:
        '${product.title}',
        % endfor
    ];
</script>