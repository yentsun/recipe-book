<%inherit file="../layout.mako"/>
<%def name="title()">${recipe.title}</%def>
<div class="span8">
        <div class="row"><blockquote class="span8" id="description">
        ${recipe.description | n}
        </blockquote></div>
    <div class="row">
    <section id="ingredients" class="span8"><h2>Ингредиенты:</h2><br>
            <ul>
                    % for ingredient in recipe.ingredients:
                        <li>${ingredient.product.title}, ${ingredient.measure()}</li>
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
                    <i class="icon-ok" style="display:none"></i> ${step.number}
                    </button>
                </td>
                <td class="text">
                % if step.time_value:
                        <span class="badge badge-info pull-right">
                    <i class="icon-time icon-white"></i> ${step.time_value} мин
                </span>
                % endif
                ${step.text | n}
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