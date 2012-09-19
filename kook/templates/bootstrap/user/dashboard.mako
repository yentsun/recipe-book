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
           class="btn btn-mini">
            <i class="icon-plus"></i> новый рецепт
        </a>
        <a href="#upload_json" data-toggle="modal"
           class="btn btn-mini">
            <i class="icon-refresh"></i> импорт из JSON
        </a>
        <div class="modal hide" id="upload_json">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">×</button>
                <h3>импорт из JSON</h3>
            </div>
            <div class="modal-body">
                <form action="${request.route_path('create_recipe')}"
                      enctype="multipart/form-data" method="post"
                      class="well form-horizontal" id="upload_form">
                    <div class="control-group">
                        <label class="control-label"
                               for="file">Файл JSON</label>
                        <div class="controls">
                            <input type="file" id="file" name="file">
                        </div>
                        <input type="hidden" name="json_upload" value="true">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <a href="#" class="btn" data-dismiss="modal">отмена</a>
                <button onclick="$('#upload_form').submit()"
                        class="btn btn-primary">
                    <i class="icon-upload icon-white"></i>
                    загрузить
                </button>
            </div>
        </div>
    </div>
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
                        <img width="25" src="${recipe.dish.image.url}"
                             alt="">
                        ${recipe.dish.title}: ${recipe.description}
                </td>
                <td>
                    ${pretty_time(recipe.creation_time)}
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

</div>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/dashboard.js"></script>
</%def>