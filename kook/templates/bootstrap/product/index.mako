<%inherit file="../layout.mako"/>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<%def name="title()">Управление продуктами</%def>
<div class="span6">
    <div class="pull-right">
        <a href="${request.route_path('create_recipe')}"
           class="btn btn-success btn-mini">
            <i class="icon-plus icon-white"></i> новый продукт</a></div>
    <h3>Все продукты <span class="badge">${len(products)}</span></h3>
    <table class="table table-striped">
        <thead>
        <tr><th></th><th></th><th></th></tr>
        </thead>
        <tbody>
                % for product in products:
                <tr>
                    <td>
                        <strong>${product.title}</strong>
                        <span style="opacity:.5">
                            ${', '.join(apu.unit.title for apu in product.APUs)}
                        </span>
                    </td>
                    <td>
                        <a title="обновить продукт" class="btn btn-mini edit"
                           href="${request.route_path('update_product',
                                                       title=product.title)}">
                            <i class="icon-pencil"></i>
                        </a>
                    </td>
                </tr>
                % endfor
        </tbody>
    </table>
</div>
<div class="span5">
    <div class="pull-right">
    <a href="${request.route_path('create_recipe')}"
       class="btn btn-success btn-mini">
        <i class="icon-plus icon-white"></i> новая мера</a></div>
    <h3>Меры  <span class="badge">${len(units)}</span></h3>
    <table class="table table-striped">
        <thead>
        <tr><th></th><th></th><th></th></tr>
        </thead>
        <tbody>
                % for unit in units:
                <tr>
                    <td>
                        ${unit.title}
                    </td>
                    <td>
                        <a title="обновить блюдо" class="btn btn-mini edit"
                           href="${request.route_path('update_dish',
                           title=unit.title)}">
                            <i class="icon-pencil"></i>
                        </a>
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