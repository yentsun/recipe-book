<%inherit file="../layout.mako"/>
<%def name="title()">Редактирование профиля</%def>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<form class="span12" action="${request.route_path('update_profile')}"
      method="post">
    <div class="row">
        <div class="span5">
            <fieldset class="well">
                <legend></legend>
                <div class="nickname">
                    <label for="nickname">псевдоним</label>
                    <input class="span5" type="text" id="nickname"
                           name="nickname" value="${profile.nickname}">
                </div>
                <div class="real_name">
                    <label for="real_name">настощее имя</label>
                    <input class="span5" type="text" id="real_name"
                           name="real_name" value="${profile.real_name}">
                </div>
                <div class="birthday">
                    <label for="birthday">дата рождения</label>
                    <input class="span5" type="text" id="birthday"
                           name="birthday" value="${profile.birthday}">
                </div>
                <div class="location">
                    <label for="location">страна/город</label>
                    <input class="span5" type="text" id="location"
                           name="location" value="${profile.location}">
                </div>
                <button type="submit" class="btn btn-success pull-right">
                    <i class="icon-ok icon-white"></i> готово
                </button>
            </fieldset>
        </div>
    </div>
</form>
<script type="text/javascript">
        % if error_data:
            var error_data = ${error_data | n};
        % endif
</script>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/register.js"></script>
</%def>