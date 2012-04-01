<%inherit file="../layout.mako"/>
<%def name="title()">Добавление рецепта</%def>
% if request.session.peek_flash():
<% flash = request.session.pop_flash() %>
% for message in flash:
   <div class="span12">${message | n}</div>
% endfor
% endif
<form class="span12" action="${create_recipe_path}" method="post">
    <div class="row">
        <div class="span6">
            <fieldset class="well">
        <legend>Название</legend>
            <label for="title">Название</label>
            <input class="span5" type="text" id="title"
                   name="title" value="" data-title="">
            <label for="description">Описание</label>
            <textarea name="description" id="description" cols="30" rows="10"></textarea>
    </fieldset>
            <fieldset class="well" id="steps_fields">
        <legend>Приготовление</legend>
##        TODO добавить пустую форму шага, если нет шагов
        <%include file="_step.mako" args="step=step"/>
        <button type="button" class="btn pull-right" id="add_step_fields">
            <i class="icon-plus"></i> шаг
        </button>
    </fieldset>
        </div>
        <div class="span6">
        <fieldset class="well" id="ingredients">
        <legend>Ингредиенты</legend>
            <table class="table table-striped">
                <thead>
                <tr>
                    <th>продукт</th>
                    <th>количество</th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
            <%include file="_ingredient.mako" args="no=1, ingredient=ingredient"/>
            </tbody></table>
            <button type="button" class="btn pull-right" id="add_ingredient_fields">
                <i class="icon-plus"></i> ингредиент
            </button>
    </fieldset>
    </div>
    </div>
    <div class="navbar navbar-fixed-bottom"><fieldset class="navbar-inner"><div class="container">
        <div class="btn-group pull-right">
        <button type="submit" class="btn btn-success" id="submit_recipe">
            <i class="icon-ok icon-white"></i> готово</button></div>
    </div></fieldset></div>
</form>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/ckeditor/ckeditor.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/ckeditor/adapters/jquery.js"></script>
    <script type="text/javascript" src="/static/bootstrap/js/bootstrap-typeahead.js"></script>
    <script type="text/javascript" src="/static/bootstrap/js/form_fields.js"></script>
    <script type="text/javascript" src="/static/bootstrap/js/add_recipe.js"></script>
</%def>
<script type="text/javascript">
    var products = [
        % for product in products:
        '${product.title}',
        % endfor
    ];
</script>