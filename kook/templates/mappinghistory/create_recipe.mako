<%inherit file="layout.mako"/>
<h1><%block name="title">Добавить рецепт</%block></h1>
% if request.session.peek_flash():
    <div id="flash">
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        ${message | n}
    % endfor
    </div>
% endif
<form class="common" action="${create_recipe_path}" method="post">
    <fieldset>
        <legend></legend>
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
        <section class="product_amount">
        <p class="product_name">
            <label for="product1">Продукт</label>
            <input id="product1" type="text" name="product" data-id="1">
        </p>
        <p class="amount">
            <label for="amount1">количество, г</label>
            <input id="amount1" type="text" name="amount">
        </p>
        </section>
        <button type="button" class="button add" id="add_ingredient_fields">
            еще ингредиент
        </button>
    </fieldset>
    <fieldset>
        <legend>Приготовление</legend>
        <section class="step">
            <label class="step_title" for="steptext_1">Шаг №<span>1</span></label>
            <input id="step1" type="hidden" name="step_number" value="1">
            <textarea name="step_text" id="steptext_1" cols="30" rows="10"></textarea>
            <p class="time_value">
                <label for="timevalue_1">время, мин</label>
                <input type="text" name="time_value" id="timevalue_1">
            </p>
            <p class="note">
                <label for="note_1">Примечание</label>
                <input type="text" name="note" id="note_1">
            </p>
        </section>
        <button type="button" class="button add" id="add_step_fields">Следующий шаг</button>
    </fieldset>
    <fieldset class="final_action">
        <button type="submit" class="button submit" id="submit_recipe">Готово</button>
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
            src="/static/mappinghistory/js/jquery-ui-1.8.18.custom.min.js"></script>
    <script type="text/javascript"
            src="/static/mappinghistory/js/ckeditor/adapters/jquery.js"></script>
    <script type="text/javascript" src="/static/mappinghistory/js/form_fields.js"></script>
    <script type="text/javascript" src="/static/mappinghistory/js/add_recipe.js"></script>
</%def>
<script type="text/javascript">
    var products = [
        % for product in products:
        '${product.title}',
        % endfor
    ];
</script>