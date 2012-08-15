<%inherit file="../layout.mako"/>
<%def name="title()">Регистрация пользователя</%def>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<form class="span12" action="${register_path}" method="post">
    <div class="row">
        <div class="span5">
            <fieldset class="well">
                Регистрация временно по приглашениям!
##                <legend></legend>
##                <div class="email">
##                    <label for="email">E-mail</label>
##                    <input class="span5" type="text" id="email"
##                           name="email" value="">
##                </div>
##                <div class="password">
##                    <label for="password">Пароль</label>
##                    <input class="span5" type="password" id="password"
##                           name="password" value="">
##                </div>
##                <button type="submit" class="btn btn-success pull-right">
##                    <i class="icon-ok icon-white"></i> готово
##                </button>
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