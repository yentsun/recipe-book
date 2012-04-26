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
        <div id="general_steps" class="span6">
            <fieldset class="well">
                <legend>Название</legend>
                <div class="title"><label for="title">Название</label>
                    <input class="span5" type="text" id="title"
                           name="title" value="" data-title="">
                </div>
                <div class="description">
                    <label for="description">Описание</label>
                    <textarea name="description" id="description"
                              cols="30" rows="10"></textarea>
                </div>
                <div class="tags">
                    <label for="tags">Категории</label>
                    <select multiple name="tag" id="tags">
                        % for tag in tags:
                        <option value="${tag.title}">${tag.title}</option>
                        % endfor
                    </select>
                </div>
                <input type="hidden">
            </fieldset>
            <fieldset class="well steps">
                <legend>Приготовление</legend>
                <div id="steps">
                    <%include file="_step.mako" args="step=None" />
                </div>
                <button id="add_step_fields" type="button"
                        class="btn pull-right">
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
                        <%include file="_ingredient.mako"
                                  args="ingredient=None" />
                    </tbody></table>
                <button type="button" class="btn pull-right"
                        id="add_ingredient_fields">
                    <i class="icon-plus"></i> ингредиент
                </button>
            </fieldset>
        </div>
    </div>
    <div class="navbar navbar-fixed-bottom">
        <fieldset class="navbar-inner">
            <div class="container">
                <div class="btn-group pull-right">
                    <button type="submit" class="btn btn-success"
                            id="submit_recipe">
                        <i class="icon-ok icon-white"></i> готово
                    </button></div>
            </div></fieldset></div>
</form>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/bootstrap-typeahead.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/add_recipe.js"></script>
</%def>
<script type="text/javascript">
    var products = [
        % for product in products:
                '${product.title}',
        % endfor
    ];
    % if error_data:
    var error_data = ${error_data | n};
    % endif
</script>