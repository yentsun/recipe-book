<%inherit file="layout.mako"/>
% if request.session.peek_flash():
    <div id="flash">
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        ${message | n}
    % endfor
    </div>
% endif
<%def name="title()">Список рецептов</%def>
<div id="text">
	% for recipe in recipes:
            <li>
                <a href="${request.route_url('read_recipe', title=recipe.title)}">${recipe.title}</a>
                (<a href="${request.route_url('update_recipe', title=recipe.title)}">редактировать</a>)
            </li>
    % endfor
</div>
<%def name="css()">
    <link rel="stylesheet" href="/static/flash-messages/main.css"
          type="text/css" media="screen" />
</%def>