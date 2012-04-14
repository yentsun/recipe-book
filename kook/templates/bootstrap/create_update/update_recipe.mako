<%inherit file="../layout.mako"/>
<%def name="title()">Обновление рецепта</%def>
<%def name="sub_title()">${recipe.title}</%def>
% if request.session.peek_flash():
<% flash = request.session.pop_flash() %>
% for message in flash:
    <div class="span12">${message | n}</div>
% endfor
% endif
<%def name="additional_buttons()">
<a class="btn pull-right" href="${request.route_path('read_recipe', title=recipe.title)}">
    <i class="icon-eye-open"></i> посмотреть рецепт
</a>
</%def>
<form class="span12" action="${update_recipe_path}" method="post">
    <div class="row">
    <div class="span6">
    <fieldset class="well">
        <legend>Название</legend>
        <div class="title"><label for="title">Название</label>
            <input class="span5" type="text" id="title"
                   name="title" value="${recipe.title}" data-title="${recipe.title}"></div>
            <div class="description"><label for="description">Описание</label>
            <textarea name="description" id="description"
                      cols="30" rows="10">
                % if recipe.description is not None:
                    ${recipe.description}
                % endif
            </textarea>
            </div>
    </fieldset>
    <fieldset class="well steps" id="steps_fields">
        <legend>Приготовление</legend>
##        TODO добавить пустую форму шага, если нет шагов
        % for step in recipe.steps:
        <%include file="_step.mako" args="step=step"/>
        % endfor
        <button type="button" class="btn pull-right" id="add_step_fields">
            <i class="icon-plus"></i> шаг
        </button>
    </fieldset>
    </div>
    <div class="span6">
    <fieldset class="well ingredients" id="ingredients">
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
            % for no, ingredient in enumerate(recipe.ingredients):
            <%include file="_ingredient.mako" args="no=no, ingredient=ingredient"/>
            % endfor
            </tbody></table>
            <button type="button" class="btn pull-right" id="add_ingredient_fields">
                <i class="icon-plus"></i> ингредиент
            </button>
    </fieldset>
    </div>
    </div>
    <div class="navbar navbar-fixed-bottom"><fieldset class="navbar-inner"><div class="container">
        <button type="button" class="btn btn-danger"
                id="delete_recipe" onclick="deleteRecipe('${recipe.title}');">
            <i class="icon-remove icon-white"></i> удалить
        </button>
        <div class="btn-group pull-right">
        <button type="button" class="btn"
                id="clone_recipe" disabled>
            <i class="icon-plus"></i> клонировать</button>
        <button type="submit" class="btn btn-success"
                id="submit_recipe">
            <i class="icon-ok icon-white"></i> обновить</button></div>
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
    <script type="text/javascript" src="/static/bootstrap/js/update_recipe.js"></script>
</%def>
<script type="text/javascript">
    var products = [
        % for product in products:
        '${product.title}',
        % endfor
    ];
</script>