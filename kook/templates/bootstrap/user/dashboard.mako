<%inherit file="../layout.mako"/>
<%! from kook.mako_filters import pretty_time %>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<%def name="title()">Панель управления</%def>
<div class="span6">
    <div class="pull-right">
        <a href="${request.route_path('create_recipe')}"
           class="btn btn-success btn-mini">
            <i class="icon-plus icon-white"></i> новый рецепт</a></div>
    <h3>Мои рецепты <span class="badge">0</span></h3>
    <table class="table table-striped" id="recipe-list">
        <thead>
        <tr>
            <th>заголовок</th>
            <th>дата</th>
        </tr>
        </thead>
        <tbody>
            ##      % for recipe in user_recipes:
##        <tr>
##          <td>
##            <a title="открыть рецепт"
##               href="${request.route_path('read_recipe',
##                                          title=recipe.title,
##                                          author_id=recipe.author.id)}">
##                ${recipe.title}
##            </a>
##            <a title="обновить рецепт" class="btn btn-mini edit"
##               href="${request.route_path('update_recipe', title=recipe.title,
##                                          author_id=recipe.author.id)}">
##                 <i class="icon-pencil"></i>
##            </a>
##          </td>
##          <td>
##              <img src="${recipe.author.gravatar_url}" alt="">
##              ${recipe.author.email}
##          </td>
##        </tr>
##      % endfor
      </tbody>
    </table>
</div>
<div class="span6">
    <h3>Избранное  <span class="badge">0</span></h3>
    <table class="table table-striped">
        <thead>
        <tr><th>название</th><th></th><th></th></tr>
        </thead>
        <tbody>
            % for recipe in all_recipes:
            <tr>
                <td>
                    <a title="открыть рецепт"
                       href="${request.route_path('read_recipe',
                                                  id=recipe.id)}">
                    ${recipe.dish.title}
                    </a>
                % if request.user is recipe.author:
                    <a title="обновить рецепт" class="btn btn-mini edit"
                       href="${request.route_path('update_recipe',
                                                  id=recipe.id)}">
                       <i class="icon-pencil"></i>
                    </a>
                % endif
                </td>
                    <td>
                        <img src="${recipe.author.gravatar_url}" alt="">
                    ${recipe.author.email}
                    </td>
                    <td>
##                        ${pretty_date(recipe.update_time)} /
##                        ${pretty_date(recipe.creation_time)}
                    </td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/dashboard.js"></script>
</%def>