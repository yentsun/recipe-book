<%inherit file="layout.mako"/>
<h1><%block name="title">Добавить рецепт</%block></h1>
<form action="${add_recipe_path}" method="post">
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
            <input id="product1" type="text" name="product" class="product_name" data-no="1">
            <input type="text" name="amount">
        </p>
        <button type="button" id="add_ingredient_fields">Добавить ингредиент</button>
    </fieldset>
    <fieldset>
        <legend>Приготовление</legend>
        <div class="phase">
            <label for="phase1">Фаза №<span>1</span></label>
            <input id="phase1" type="hidden" name="phase_no" value="1">
            <ul class="ingredients_list"></ul>
            <input type="hidden" name="ingredients">
            <input type="text" name="action">
            <input type="text" name="time_value">
            <input type="text" name="note">
        </div>
        <button type="button" id="add_phase_fields">Добавить фазу</button>
    </fieldset>
    <fieldset>
        <button type="submit">Добавить</button>
    </fieldset>
</form>
<%def name="js()">
    <script type="text/javascript" src="/static/js/add_recipe.js"></script>
</%def>