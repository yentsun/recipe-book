# -*- coding: utf-8 -*-
<%inherit file="../layout.mako"/>
<%! from kook.mako_filters import pretty_time %>
% if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    % for message in flash:
        <div class="span12">${message | n}</div>
    % endfor
% endif
<%def name="title()">Главная</%def>
<div class="span5 left">
    <div id="dish_slides">
    % for dish in popular_dishes:
        <div class="item"
             style="background-image:url(${dish.image.url})">
            <div class="caption">
                <h3>${dish.title}
                    <span class="badge badge-inverse">
                        ${len(dish.recipes)}
                    </span>
                </h3>
            </div>
        </div>
    % endfor
    </div>
</div>
<div class="span6 right">
    <input disabled placeholder="искать рецепт..." type="text" id="search-query">
    <h3>Лучшие рецепты</h3>
    <table id="best-recipes" class="table table-striped">
        <tbody>
            % for recipe in best_recipes:
            <tr>
                <td>
                    <div class="icon">
                    <img width="25" src="${recipe.dish.image.url}"
                         alt="">
                    </div>
                </td>
                <td>
                    <strong>${recipe.rating}</strong>
                </td>
                <td>
                    <a title="открыть рецепт"
                       href="${request.route_path('read_recipe',
                       id=recipe.id)}">
                    ${recipe.dish.title}
                    </a>
                </td>
                <td>
                    <img src="${recipe.author.gravatar_url()}" alt="">
                    ${recipe.author.display_name}
                    <strong>${recipe.author.profile.rep}</strong>
                </td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>
    <div class="span8">
        <div class="page-header">
            <h3>Категории</h3>
        </div>
        <div class="span2">
            <ul>
                <li><a href="${request.route_path('tag', title=u'салаты')}">
                    салаты
                </a></li>
                <li><a href="${request.route_path('tag', title=u'супы')}">
                    супы
                </a></li>
                <li><a href="${request.route_path('tag', title=u'гарниры')}">
                    гарниры
                </a></li>
                <li><a href="${request.route_path('tag', title=u'основные блюда')}">
                    основные блюда
                </a></li>
                <li><a href="${request.route_path('tag', title=u'десерты')}">
                    десерты
                </a></li>
                <li><a href="${request.route_path('tag', title=u'напитки')}">
                    напитки
                </a></li>
            </ul>
        </div>
        <div class="span2">
            <ul>
                <li>
                    <a href="${request.route_path('tag', title=u'русская кухня')}">
                        русская
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'европейская кухня')}">
                        европейская
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'кавказская кухня')}">
                        кавказская
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'латиноамериканская кухня')}">
                        латиноамериканская
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'восточная кухня')}">
                        восточная
                    </a>
                </li>
            </ul>
        </div>
        <div class="span2">
            <ul>
                <li>
                    <a href="${request.route_path('tag', title=u'быстрое')}">
                        быстрые
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'дешевое')}">
                        дешевые
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'праздничное')}">
                        праздничные
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'низкокалорийное')}">
                        низкокалорийные
                    </a>
                </li>
                <li>
                    <a href="${request.route_path('tag', title=u'высококалорийное')}">
                        высококалорийные
                    </a>
                </li>
            </ul>
        </div>
    </div>
<div class="span3">
    <h3>топ 10 поваров</h3>
    <table id="best-users" class="table table-striped">
        <tbody>
                % for user in best_users:
                <tr>
                    <td>
                        <img src="${user.gravatar_url()}" alt="">
                        ${user.display_name}
                        <strong>${user.profile.rep}</strong>
                    </td>
                </tr>
                % endfor
        </tbody>
    </table>
</div>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/index.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/jquery.cycle.all.latest.js"></script>
</%def>