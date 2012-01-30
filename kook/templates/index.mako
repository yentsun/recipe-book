<%inherit file="layout.mako"/>
<%def name="title()">Список рецептов</%def>
<div id="text">
	% for recipe in recipes:
            <li><a title="${recipe.description}" href="${request.route_url('recipe', title=recipe.title)}">${recipe.title}</a></li>
    % endfor
</div>
