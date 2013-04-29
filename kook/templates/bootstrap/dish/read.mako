<%inherit file="../layout.mako"/>
<%!
    from kook.mako_filters import markdown, pretty_time
    from kook.models import form_msg
    from pyramid.security import (has_permission,
                                  principals_allowed_by_permission)
%>
<%def name="body_id()">read_dish</%def>
<%def name="title()">${dish.title}</%def>
<%def name="sub_title()">
    ${', '.join([tag.title for tag in dish.tags])}
</%def>
<div class="page-header">
    <h1 id="dish-title" class="">
        ${self.title()}
        <span class="badge badge-inverse" title="Количество рецептов">
            ${len(dish.recipes)}
        </span>
        % if hasattr(self,'sub_title'):
        <br>
        <small>${self.sub_title()}</small>
        % endif

    </h1>
</div>
<div class="row-fluid">
    <div id="dish_image" class="span6">
        <img width="100%" src="${dish.image.url}" alt="">
        <div id="photo_credit">
            Фото: ${dish.image.credit or dish.image.get_credit()}
        </div>
    </div>
    <div id="dish_secription" class="span6">
        <div id="description">${dish.description | markdown}</div>
    </div>
</div>
<div class="row-fluid">
    <div class="span12" id="recipe-list">
        <h3>Рецепты</h3>
        <table class="table table-striped">
            <tbody>
                % for recipe in dish.recipes:
                <tr>
                    <td title="Рейтинг рецепта">
                        <strong class="label">
                            ${recipe.fetch_rating()}
                        </strong>
                    </td>
                    <td>
                        <a class="description"
                           title="открыть рецепт"
                           href="${request.route_path('read_recipe',
                                                      id=recipe.ID)}">
                        ${recipe.description}
                        </a>
                    </td>
                    <td title="время приготовления">
                        <span class="badge">
                            <i class="icon-time icon-white"></i>
                            % if recipe.total_time.hour:
                            ${recipe.total_time.hour} ч
                            % endif
                            % if recipe.total_time.minute:
                            ${recipe.total_time.minute} мин
                            % endif
                        </span>
                    </td>
                    <td title="Кол-во игредиентов и шагов приготовления">
                        ${len(recipe.ingredients)} ингр. /
                        ${len(recipe.steps)} шаг.
                    </td>
                    <td title="автор">
                        <img src="${recipe.author.gravatar_url()}" alt="">
                    ${recipe.author.display_name}
                        <strong>${recipe.author.fetch_rep()}</strong>
                    </td>
                    <td title="дата создания / обновления">
                        ${pretty_time(recipe.update_time) or\
                          pretty_time(recipe.creation_time)}
                    </td>
                </tr>
                % endfor
            </tbody>
        </table>
    </div>
</div>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/bootstrap-button.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/read_dish.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/jquery.jeditable.mini.js"></script>
</%def>
% if request.user:
<script type="text/javascript">
    var user = ${request.user.to_json() | n};
</script>
% endif