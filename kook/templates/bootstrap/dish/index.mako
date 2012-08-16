<%inherit file="../layout.mako"/>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<%def name="title()">Управление блюдами</%def>
<div class="span6">
    <div class="pull-right">
        <a href="${request.route_path('create_dish')}"
           class="btn btn-success btn-mini">
            <i class="icon-plus icon-white"></i> новое блюдо</a></div>
    <h3>Все блюда <span class="badge">${len(dishes)}</span></h3>
    <table class="table table-striped">
        <thead>
        <tr><th></th><th></th><th></th></tr>
        </thead>
        <tbody>
                % for dish in dishes:
                <tr>
                <td>
                % if dish.image:
                        <img width="25" src="${dish.image.url}" alt="">
                % endif
                ${dish.title}
                    <small style="opacity:.5">
                    ${', '.join([tag.title for tag in dish.tags])}
                    </small>
                </td>
                    <td>
                        <a title="обновить блюдо" class="btn btn-mini edit"
                           href="${request.route_path('update_dish',
                           title=dish.title)}">
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
            src="/static/bootstrap/js/dishes.js"></script>
</%def>