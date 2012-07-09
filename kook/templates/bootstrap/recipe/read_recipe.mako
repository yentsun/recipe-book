<%inherit file="../layout.mako"/>
<%!
    from kook.mako_filters import markdown, pretty_time
    from kook.models import form_msg
    from pyramid.security import (has_permission,
                                  principals_allowed_by_permission)
%>
<%def name="body_id()">read_recipe</%def>
<%def name="title()">${recipe.dish.title}</%def>
<%def name="sub_title()">
    — ${recipe.description} от
    <span class="well">
        <img src="${recipe.author.gravatar_url(30)}" alt="юзерпик">
    ${recipe.author.display_name}
        <strong>${recipe.author.profile.rep}</strong>
        </span>
</%def>
<div class="page-header">
    <h1 class="recipe-title"> ${self.title()}
        % if hasattr(self,'sub_title'):
                <small>${self.sub_title()}</small>
        % endif
    </h1>
    % if hasattr(self,'additional_buttons'):
        ${self.additional_buttons()}
    % endif
</div>
<div class="row">
    <div class="span1" class="toolbox">
        <div id="voting" class="pull-left">
            % if last_vote and last_vote.value is UPVOTE:
            <button class="btn btn-success active" type="button"
                    data-toggle="button"
                    data-original-title="Вы уже проголосовали: +1">
                <i class="icon-chevron-up icon-white"></i>
            </button>
            % else:
            <button class="btn" type="button"
                    data-toggle="button"
                % if can_upvote:
                    onclick="vote(${UPVOTE}, '${recipe.id}', this)"
                % else:
                    data-original-title="${form_msg(can_upvote)}"
                % endif
                >
                <i class="icon-chevron-up"></i>
            </button>
            % endif
            <div id="rating_value" class="well">${recipe.rating}</div>
            % if last_vote and last_vote.value is DOWNVOTE:
            <button class="btn btn-warning active" type="button"
                    data-original-title="Вы уже проголосовали: -1"
                    data-toggle="button">
                <i class="icon-chevron-down"></i>
            </button>
            % else:
            <button class="btn" type="button" data-toggle="button"
                % if can_downvote:
                    onclick="vote(${DOWNVOTE}, '${recipe.id}', this)"
                % else:
                    data-original-title="${form_msg(can_downvote)}"
                % endif
                >
                <i class="icon-chevron-down"></i>
            </button>
            % endif

        </div>
        % if can_update:
        <a title="обновить рецепт" class="btn edit"
           href="${request.route_path('update_recipe',
           id=recipe.id)}">
            <i class="icon-pencil"></i>
        </a>
        % endif
    </div>
    <div class="span5">
        <div>
            <img width="470" src="${recipe.dish.image.url}" alt="">
        </div>
        <div id="photo_credit">
            Фото: ${recipe.dish.image.credit or recipe.dish.image.get_credit()}
        </div>
    </div>
    <div class="span3">
        <section id="ingredients">
            <h3>Ингредиенты:</h3><br>
            <ul>
                % for ingredient in recipe.ingredients:
                <li>${ingredient.product.title},
                    ${ingredient.measured}
                    % if ingredient.unit:
                    <span title="${ingredient.unit.title}">
                        ${ingredient.unit.abbr}
                    </span>
                    % else:
                        <span title="грамм">г</span>
                    % endif
                </li>
                % endfor
            </ul>
        </section>
    </div>
    <div class="span8 offset1">
        <div id="steps"><h3>Приготовление:</h3><br>
            <table class="table table-striped" cellpadding="0" cellspacing="0">
                % for step in recipe.steps:
                <tr>
                    <td class="no">
                            <button class="btn btn-primary"
                                    data-toggle="button">
                            ${step.number} <i class="icon-ok icon-white"
                                              style="display:none"></i>
                            </button>
                        </td>
                    <td class="text">
                    % if step.time_value:
                        <span class="badge badge-info pull-right">
                            <i class="icon-time icon-white"></i>
                            ${step.time_value} мин
                        </span>
                    % endif
                    ${step.text | markdown, n}
                    </td>
                </tr>
                %endfor
            </table>
        </div>
        <div id="comments">
            % if len(recipe.comments) > 0:
            <h3>
                комментарии
                <span class="badge">${len(recipe.comments)}</span>
            </h3>
            % endif
            <div id="comment_list">
                % for comment in recipe.comments:
                <%
                    comment.attach_acl()
                    can_edit = has_permission('delete', comment, request)
                %>
                <%include file="_comment.mako" args="comment=comment,
                                                     can_edit=can_edit" />
                % endfor
            </div>
            % if can_comment:
            <div id="comment_form">
            <textarea name="text" id="comment_text"
                      placeholder="Ваш комментарий (не менее 15 символов)"
                      cols="60" rows="10"></textarea>
            <button class="btn"
                    onclick="post_comment('${recipe.id}')">
                отправить
            </button>
            </div>
            % else:
            <p id="cant_comment">
                <span class="label">
                <i class="icon-info-sign icon-white"></i>
                    зарегистрируйтесь чтобы добавить комментарий
                </span>
            </p>
            % endif
        </div>
    </div>
</div>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/bootstrap-button.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/read_recipe.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/jquery.jeditable.mini.js"></script>
</%def>
% if request.user:
<script type="text/javascript">
    var user = ${request.user.to_json() | n};
</script>
% endif