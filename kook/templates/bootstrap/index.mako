<%inherit file="layout.mako"/>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        ${message | n}
    % endfor
% endif
<%def name="title()">Панель управления</%def>
<div class="row">
  <div class="span6">
    <div class="pull-right">
          <a href="${request.route_path('create_recipe')}" class="btn btn-success btn-mini">
              <i class="icon-plus icon-white"></i> новый рецепт</a></div>
    <h3>Рецепты <span class="badge">${len(recipes)}</span></h3>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>заголовок</th>
          <th>дата</th>
        </tr>
      </thead>
      <tbody>
      % for recipe in recipes:
        <tr>
          <td>
            <a title="редактировать"
               href="${request.route_path('update_recipe', title=recipe.title)}">${recipe.title}</a>
          </td>
          <td></td>
        </tr>
      % endfor
      </tbody>
    </table>
  </div>
  <div class="span6">
    <h3>Продукты  <span class="badge">${len(products)}</span></h3>
    <table class="table table-striped">
      <thead>
        <tr><th>название</th><th>единицы измерения</th></tr>
      </thead>
      <tbody>
      % for product in products:
        <tr>
          <td>${product.title}</td>
          <td></td>
        </tr>
      % endfor
      </tbody>
    </table>
  </div>
</div>