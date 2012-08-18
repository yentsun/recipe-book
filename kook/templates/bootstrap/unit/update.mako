<%!
    from pyramid.security import has_permission
%>
<%inherit file="../layout.mako"/>
<%def name="title()">Обновление меры</%def>
<%def name="sub_title()">${unit.title}</%def>
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
<form class="span12" action="${submit_path}" method="post">
    <div class="row">
        <div class="span6">
            <fieldset class="well">
                <legend>Название</legend>
                <div class="unit_title">
                    <label for="title">Название</label>
                    <input class="span5" type="text" id="title"
                           name="title"
                           value="${unit.title}">
                </div>
                <div>
                    <label for="abbr">Сокращение</label>
                    <input class="span5" type="text" id="abbr"
                           name="abbr"
                           value="${unit.abbr}">
                </div>
            </fieldset>
        </div>
        <div class="span6">
        </div>
    </div>
    <div class="navbar navbar-fixed-bottom">
        <fieldset class="navbar-inner"><div class="container">
            <div class="btn-group pull-right">
                <button type="submit" class="btn btn-success"
                        id="submit_unit">
                    <i class="icon-ok icon-white"></i> обновить</button>
            </div>
        </div></fieldset></div>
</form>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/markitup/jquery.markitup.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/markitup/sets/markdown/set.js"></script>
</%def>
<%def name="css()">
    <link rel="stylesheet" type="text/css"
          href="/static/bootstrap/js/markitup/skins/simple/style.css">
    <link rel="stylesheet" type="text/css"
          href="/static/bootstrap/js/markitup/sets/markdown/style.css" />
</%def>
<script type="text/javascript">
</script>