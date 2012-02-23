<%inherit file="layout.mako"/>
<h1><%block name="title">Добавить рецепт</%block></h1>
<form action="${create_recipe_path}" method="post">
    <fieldset>
        <legend>Общая информация</legend>
        <p>
            <label for="title">Название</label>
            <input type="text" id="title" name="title">
        </p>
        <p>
            <label for="description">Описание</label>
            <textarea name="description" id="description" cols="30" rows="10"></textarea>
        </p>
    </fieldset>
    <fieldset>
        <legend>Ингредиенты</legend>
        <p class="product_amount">
            <label for="product1">Продукт, количество в г</label>
            <input id="product1" type="text" name="product" class="product_name" data-id="1">
            <input type="text" name="amount">
        </p>
        <button type="button" id="add_ingredient_fields">Следующий ингредиент</button>
    </fieldset>
    <fieldset>
        <legend>Приготовление</legend>
        <div class="step">
            <label class="step_title" for="steptext_1">Шаг №<span>1</span></label>
            <input id="step1" type="hidden" name="step_number" value="1">
            <textarea name="step_text" id="steptext_1" cols="30" rows="10"></textarea>
            <input type="text" name="time_value">
        </div>
        <button type="button" id="add_step_fields">Следующий шаг</button>
    </fieldset>
    <fieldset>
        <button type="submit">Готово</button>
    </fieldset>
</form>
<%def name="js()">
    <script type="text/javascript" src="/static/js/ckeditor/ckeditor.js"></script>
    <script type="text/javascript" src="/static/js/ckeditor/adapters/jquery.js"></script>
    <script type="text/javascript" src="/static/js/form_fields.js"></script>
    <script type="text/javascript" src="/static/js/add_recipe.js"></script>
</%def>