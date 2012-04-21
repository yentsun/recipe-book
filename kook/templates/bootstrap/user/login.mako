<%inherit file="../layout.mako"/>
<%def name="title()">Авторизация</%def>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<form class="span12" action="${request.route_path('login')}" method="post">
    <div class="row">
        <div class="span5">
            <fieldset class="well">
                <legend></legend>
                <div class="email">
                    <label for="email">E-mail</label>
                    <input class="span5" type="text" id="email"
                           name="email" value="">
                </div>
                <div class="password">
                    <label for="password">Пароль</label>
                    <input class="span5" type="password" id="password"
                           name="password" value="">
                </div>
                <a href="${request.route_path('register_user')}">
                    регистрация
                </a> |
                <a href="${request.route_path('register_user')}">
                    забыли пароль?
                </a>
                <button type="submit" class="btn btn-primary pull-right">
                    <i class="icon-chevron-right icon-white"></i> войти
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