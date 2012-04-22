<%inherit file="../layout.mako"/>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<%def name="title()">Панель управления</%def>
  <div class="span6">
    <div class="pull-right">
          <a href="${request.route_path('create_recipe')}" class="btn btn-success btn-mini">
              <i class="icon-plus icon-white"></i> новый рецепт</a></div>
    <h3>Мои рецепты <span class="badge">${len(user_recipes)}</span></h3>
    <table class="table table-striped" id="recipe-list">
      <thead>
        <tr>
          <th>заголовок</th>
          <th>дата</th>
        </tr>
      </thead>
      <tbody>
      % for recipe in user_recipes:
        <tr>
          <td>
            <a title="открыть рецепт"
               href="${request.route_path('read_recipe',
                                          title=recipe.title,
                                          author_id=recipe.author.id)}">
                ${recipe.title}
            </a>
            <a title="обновить рецепт" class="btn btn-mini edit"
               href="${request.route_path('update_recipe', title=recipe.title,
                                          author_id=recipe.author.id)}">
                 <i class="icon-pencil"></i>
            </a>
          </td>
          <td>
              <img src="${recipe.author.gravatar_url}" alt="">
              ${recipe.author.email}
          </td>
        </tr>
      % endfor
      </tbody>
    </table>
  </div>
  <div class="span6">
    <h3>Избранное  <span class="badge">0</span></h3>
    <table class="table table-striped">
      <thead>
        <tr><th>название</th><th>единицы измерения</th></tr>
      </thead>
      <tbody>
##      % for product in products:
##        <tr>
##          <td>${product.title}</td>
##          <td></td>
##        </tr>
##      % endfor
      </tbody>
    </table>
  </div>
<%def name="js()">
    <script type="text/javascript" src="/static/bootstrap/js/dashboard.js"></script>
</%def>