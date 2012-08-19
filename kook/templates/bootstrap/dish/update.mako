<%!
    from pyramid.security import has_permission
%>
<%inherit file="../layout.mako"/>
<%def name="title()">Обновление блюда</%def>
<%def name="sub_title()">${dish.title}</%def>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<div class="page-header">
    <h1>${self.title()}
        % if hasattr(self,'sub_title'):
        <small>${self.sub_title()}</small>
        % endif
    </h1>
</div>
<form class="span12" action="${update_dish_path}" method="post">
    <div class="row">
        <div class="span6">
            <fieldset class="well">
                <legend>Название</legend>
                <div class="dish_title">
                    <label for="dish_title">Название</label>
                    <input class="span5" type="text" id="dish_title"
                           name="title"
                           value="${dish.title}">
                </div>
                <div class="description">
                    <label for="description">Описание</label>
                    <textarea name="description" id="description"
                              cols="30"
                              rows="10">${dish.description}</textarea>
                </div>
                <div class="tags">
                    <label for="tags">Категории</label>
                    <select data-placeholder="выберите одну или несколько"
                            class="span5" multiple name="tag" id="tags">
                    % for tag in tags:
                        <option value="${tag.title}"
                                % if tag in dish.tags:
                            selected
                                % endif
                        >
                        ${tag.title}
                        </option>
                    % endfor
                    </select>
                </div>
                <div class="image_url">
                    <label for="image_url">Адрес изображения</label>
                    <input class="span5" type="text" id="image_url"
                           name="image_url"
                           value="${dish.image.url}">
                </div>
                <div class="image_credit">
                    <label for="image_credit">Авторство изображения</label>
                    <input class="span5" type="text" id="image_credit"
                           name="image_credit"
                           value="${dish.image.credit}">
                </div>
            </fieldset>
        </div>
        <div class="span6">
            <div id="image">
                <h3>Изображение</h3>
                <img style="max-width:530px" src="${dish.image.url}" alt="">
            </div>
        </div>
    </div>
    <div class="navbar navbar-fixed-bottom">
        <fieldset class="navbar-inner"><div class="container">
            % if has_permission('delete', 'dish', request):
            <button type="button" class="btn btn-danger"
                    id="delete_dish"
                    onclick="deleteDish('${dish.title}');">
                <i class="icon-remove icon-white"></i> удалить
            </button>
            % endif
            <div class="btn-group pull-right">
                <button type="submit" class="btn btn-success"
                        id="submit_dish">
                    <i class="icon-ok icon-white"></i> обновить</button>
            </div>
        </div></fieldset></div>
</form>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/update_dish.js"></script>
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
</script>