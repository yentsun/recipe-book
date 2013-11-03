# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>
<%def name="title()">Главная</%def>
<%def name="js()"></%def>
<section id="recently_added">
    <hr>
    <h2>Новые рецепты</h2>
    <ul class="thumbnails">
    % for recipe in recent:
     <%include file="_recipe_preview.mako" args="recipe=recipe" />
    % endfor
    </ul>
</section>
<section id="categories">
    <hr>
    <h2>Категории блюд</h2>
    <div>
        <ul>
            <li><a href="${request.route_path('tag', title=u'салаты')}">
                салаты
            </a></li>
            <li><a href="${request.route_path('tag', title=u'закуски')}">
                закуски
            </a></li>
            <li><a href="${request.route_path('tag', title=u'первые блюда')}">
                первые блюда
            </a></li>
            <li><a href="${request.route_path('tag', title=u'основные блюда')}">
                основные блюда
            </a></li>
            <li><a href="${request.route_path('tag', title=u'гарниры')}">
                гарниры
            </a></li>
            <li><a href="${request.route_path('tag', title=u'заправки')}">
                заправки
            </a></li>
            <li><a href="${request.route_path('tag', title=u'выпечка')}">
                выпечка
            </a></li>
            <li><a href="${request.route_path('tag', title=u'десерты')}">
                десерты
            </a></li>
            <li><a href="${request.route_path('tag', title=u'напитки')}">
                напитки
            </a></li>
        </ul>
    </div>
    <div>
        <ul>
            <li>
                <a href="${request.route_path('tag', title=u'славянская кухня')}">
                    славянская
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
                <a href="${request.route_path('tag', title=u'азиатская кухня')}">
                    азиатская
                </a>
            </li>
            <li>
                <a href="${request.route_path('tag', title=u'восточная кухня')}">
                    восточная
                </a>
            </li>
        </ul>
    </div>
    <div>
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
                <a href="${request.route_path('tag', title=u'вегетарианская кухня')}">
                    вегетарианская кухня
                </a>
            </li>
        </ul>
    </div>
</section>