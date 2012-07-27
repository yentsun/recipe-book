<%inherit file="../layout.mako"/>
<%def name="title()">Обновление продукта</%def>
<%def name="sub_title()">${product.title}</%def>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<form class="span12" action="${update_path}" method="post">
    <div class="row">
        <div class="span6">
            <fieldset class="well">
                <legend>Название</legend>
                <div class="product_title">
                    <label for="title">Название</label>
                    <input class="span5" type="text" id="title"
                           name="title"
                           value="${product.title}">
                </div>
                <div class="description">
                    <label for="description">Описание</label>
                    <textarea name="description" id="description" disabled
                              cols="30"
                              rows="10"></textarea>
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
                        id="submit_product">
                    <i class="icon-ok icon-white"></i> обновить</button>
            </div>
        </div></fieldset></div>
</form>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/update_product.js"></script>
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