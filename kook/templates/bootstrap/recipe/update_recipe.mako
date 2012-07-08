<%inherit file="../layout.mako"/>
<%!
    from kook.mako_filters import failsafe_get as get
    from pyramid.security import (has_permission,
                                  principals_allowed_by_permission)
%>
<%def name="title()">Обновление рецепта</%def>
<%def name="sub_title()">${recipe.dish.title}</%def>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<%def name="additional_buttons()">
    <div class="btn-group pull-right">
        <a class="btn"
           href="${request.route_path('read_recipe', id=recipe.id,
           author_id=request.user.id)}">
            <i class="icon-eye-open"></i> посмотреть на сайте
        </a>
        <button id="toggle-status" class="btn btn-warning"
                data-toggle="button" data-original-title="Скрытый рецепт не
                будет виден никому кроме вас">
            <i class="icon-eye-close"></i> скрыть
        </button>
    </div>
</%def>
<form class="span12" action="${update_recipe_path}" method="post">
    <div class="row">
        <div class="span6">
            <fieldset class="well">
                <legend>Название</legend>
                <div class="dish_title">
                    <label for="dish_title">Название</label>
                    <input class="span5" type="text" id="dish_title"
                           name="dish_title"
                           value="${get(recipe, 'dish.title')}"
                           data-title="${get(recipe, 'dish.title')}"></div>
                <div class="description">
                    <label for="description">
                        В "двух словах": чем уникален этот рецепт?
                    </label>
                    <textarea name="description" id="description"
                              cols="30"
                              rows="10">
${get(recipe, 'description')}</textarea>
                </div>
##                <div class="tags">
##                    <label for="tags">Категории</label>
##                    <select data-placeholder="выберите одну или несколько"
##                            class="span5" multiple name="tag" id="tags">
##                    % for tag in tags:
##                        <option value="${tag.title}"
##                                % if tag in recipe.tags:
##                            selected
##                                % endif
##                        >
##                        ${tag.title}
##                        </option>
##                    % endfor
##                    </select>
##                </div>
            </fieldset>
            <fieldset id="hidden-fields">
                <legend></legend>
                <input type="hidden" name="status_id"
                       value="${get(recipe, 'status_id')}">
            </fieldset>
            <fieldset class="well steps" id="steps_fields">
                <legend>Приготовление</legend>
                <div id="steps">
                % if data and data['steps']:
                    % for step in data['steps']:
                    <%include file="_step.mako" args="step=step" />
                    % endfor
                % else:
                    % for step in recipe.steps:
                    <%include file="_step.mako" args="step=step"/>
                    % endfor
                % endif
                </div>
                <button type="button" class="btn pull-right"
                        id="add_step_fields">
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
                    % if data and data['ingredients']:
                        % for ingredient in data['ingredients']:
                        <%include file="_ingredient.mako"
                                  args="ingredient=ingredient"/>
                        % endfor
                    % else:
                        % for ingredient in recipe.ingredients:
                        <%include file="_ingredient.mako"
                                  args="ingredient=ingredient"/>
                        % endfor
                    % endif
                    </tbody></table>
                <button type="button" class="btn pull-right"
                        id="add_ingredient_fields">
                    <i class="icon-plus"></i> ингредиент
                </button>
            </fieldset>
        </div>
    </div>
    <div class="navbar navbar-fixed-bottom">
        <fieldset class="navbar-inner"><div class="container">
            % if has_permission('delete', recipe, request):
            <button type="button" class="btn btn-danger"
                    id="delete_recipe"
                    onclick="deleteRecipe('${recipe.id}');">
                <i class="icon-remove icon-white"></i> удалить
            </button>
            % endif
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
            src="/static/bootstrap/js/bootstrap-typeahead.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/add_recipe.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/update_recipe.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/chosen/chosen.jquery.min.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/markitup/jquery.markitup.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/markitup/sets/markdown/set.js"></script>
</%def>
<%def name="css()">
    <link href="/static/bootstrap/js/chosen/chosen.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css"
          href="/static/bootstrap/js/markitup/skins/simple/style.css">
    <link rel="stylesheet" type="text/css"
          href="/static/bootstrap/js/markitup/sets/markdown/style.css" />
</%def>
<script type="text/javascript">
    var recipe_id = '${recipe.id}';
    var products = [
        % for product in products:
                '${product.title}',
        % endfor
    ];
        % if errors:
            var error_data = ${errors | n};
        % endif
</script>