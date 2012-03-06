<%inherit file="layout.mako"/>
<%def name="title()">Список рецептов</%def>
<div id="text">
	% for recipe in recipes:
            <li>
                <a href="${request.route_url('read_recipe', title=recipe.title)}">${recipe.title}</a>
                (<a href="${request.route_url('update_recipe', title=recipe.title)}">редактировать</a>)
            </li>
    % endfor
</div>
