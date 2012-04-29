<%inherit file="../layout.mako"/>
<%!
    from kook.mako_filters import markdown
%>
<%def name="title()">${recipe.title}</%def>
<%def name="sub_title()">
    ${', '.join([tag.title for tag in recipe.tags])}
</%def>
<div class="span8">
    <div class="row">
            % if recipe.description is not None:
                <blockquote class="span8"
                            id="description">
                ${recipe.description | markdown, n}
                </blockquote>
            % endif
    </div>
    <div class="row">
        <section id="ingredients" class="span8"><h2>Ингредиенты:</h2><br>
            <ul>
                    % for ingredient in recipe.ingredients:
                    <li>${ingredient.product.title},
                    ${ingredient.measured}
                    % if ingredient.unit is not None:
                        <span title="${ingredient.unit.title}">
                            ${ingredient.unit.abbr}
                        </span>
                    % else:
                        <span title="грамм">г</span>
                    % endif
                    </li>
                    % endfor
            </ul>
        </section></div>
    <div class="row">
        <section id="steps" class="span8"><h2>Приготовление:</h2><br>
            <table class="table table-striped" cellpadding="0" cellspacing="0">
                    % for step in recipe.steps:
                    <tr>
                        <td class="no">
                            <button class="btn" data-toggle="button">
                            ${step.number} <i class="icon-ok" style="display:none"></i>
                            </button>
                        </td>
                    <td class="text">
                    % if step.time_value:
                            <span class="badge badge-info pull-right">
                    <i class="icon-time icon-white"></i> ${step.time_value} мин
                </span>
                    % endif
                    ${step.text | markdown, n}
                    </td>
                    </tr>
                    %endfor
            </table>
        </section>
    </div>
</div>
<%def name="js()">
    <script type="text/javascript" src="/static/bootstrap/js/bootstrap-button.js"></script>
    <script type="text/javascript" src="/static/bootstrap/js/read_recipe.js"></script>
</%def>