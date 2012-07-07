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
    <h3>Мои рецепты <span class="badge">${len(user_recipes)}</span></h3>
    <table class="table table-striped">
        <thead>
        <tr><th></th><th></th><th></th></tr>
        </thead>
        <tbody>
            % for recipe in user_recipes:
            <tr>
                <td>
                    <strong class="label">
                    ${recipe.rating}
                    </strong>
                </td>
                <td>
                    <a title="открыть рецепт"
                       href="${request.route_path('read_recipe',
                                                  id=recipe.id)}">
                        <img width="25" src="${recipe.dish.image.url}"
                             alt="">
                        ${recipe.dish.title}: ${recipe.description}
                    </a>
                </td>
                <td>
                    ${pretty_time(recipe.update_time) or\
                      pretty_time(recipe.creation_time)}
                </td>
                <td>
                    <a title="обновить рецепт" class="btn btn-mini edit"
                           href="${request.route_path('update_recipe',
                           id=recipe.id)}">
                            <i class="icon-pencil"></i>
                    </a>
                </td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>
<div class="span5">
    <h3>Избранное  <span class="badge">0</span></h3>

</div>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/dashboard.js"></script>
</%def>