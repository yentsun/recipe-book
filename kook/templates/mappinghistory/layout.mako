<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>${self.title()} - база рецептов "Kook"</title>
    <link rel="icon" type="image/png"
          href="/static/img/favicon.png" />
    <link rel="stylesheet" href="/static/mappinghistory/styles.css"
          type="text/css" media="screen" />
    <link rel="stylesheet" type="text/css" href="/static/mappinghistory/print.css"
          media="print" />
    <!--[if IE]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
    % if hasattr(self,'css'):
        ${self.css()}
    % endif
</head>
<body>
<div id="wrapper"><!-- #wrapper -->
    <header><!-- header -->
        <h2>база рецептов</h2>
        <img src="/static/img/logo.png" width="200" height="246" alt="Лого">
    </header><!-- end of header -->

    <nav><!-- top nav -->
        <div class="menu">
            <ul>
                % for title, path in request.nav.items():
                <li>
                % if path == request.path:
                <span class="${title}">${title}</span>
                % else:
                <a class="${title}" href="${path}">${title}</a>
                % endif
                </li>
                % endfor
            </ul>
        </div>
    </nav><!-- end of top nav -->


    <section id="main"><!-- #main content and sidebar area -->
        <section id="container"><!-- #container -->
            <section id="content"><!-- #content -->
                ${next.body()}
            </section><!-- end of #content -->
        </section><!-- end of #container -->

        <aside id="sidebar"><!-- sidebar -->
            <h3>Недавние рецепты</h3>
            <ul class="recipe_list">
                %for recipe in recipes:
                <li>
                    <a href="${request.route_url('read_recipe',
                                                 title=recipe.title)}">
                        ${recipe.title}</a>
                    <a class="edit" title="Редактировать рецепт"
                       href="${request.route_url('update_recipe',
                                                 title=recipe.title)}"></a>
                </li>
                %endfor
            </ul>
        </aside><!-- end of sidebar -->

    </section><!-- end of #main content and sidebar-->

    <footer>
        <section id="footer-area">

            <section id="footer-outer-block">
                <aside id="first" class="footer-segment">
                    <h3>Explore More</h3>
                    <ul>
                        <li><a href="#">one linkylink</a></li>
                        <li><a href="#">two linkylinks</a></li>
                        <li><a href="#">three linkylinks</a></li>
                        <li><a href="#">four linkylinks</a></li>
                        <li><a href="#">five linkylinks</a></li>
                    </ul>
                </aside><!-- end of #first footer segment -->

                <aside id="second" class="footer-segment">
                    <h3>Our Most Popular</h3>
                    <ul>
                        <li><a href="#">one linkylink</a></li>
                        <li><a href="#">two linkylinks</a></li>
                        <li><a href="#">three linkylinks</a></li>
                        <li><a href="#">four linkylinks</a></li>
                        <li><a href="#">five linkylinks</a></li>
                    </ul>
                </aside><!-- end of #second footer segment -->

                <aside id="third" class="footer-segment">
                    <h3>Just The Basics</h3>
                    <ul>
                        <li><a href="#">one linkylink</a></li>
                        <li><a href="#">two linkylinks</a></li>
                        <li><a href="#">three linkylinks</a></li>
                        <li><a href="#">four linkylinks</a></li>
                        <li><a href="#">five linkylinks</a></li>
                    </ul>
                </aside><!-- end of #third footer segment -->

                <aside id="fourth" class="footer-segment">
                    <h3>Статистика</h3>
                    <p>
                        Всего рецептов в базе: ${len(recipes)}<br>
                        Всего продуктов в базе: ${len(products)}<br>
                    </p>
                </aside><!-- end of #fourth footer segment -->

            </section><!-- end of #footer-outer-block -->

        </section><!-- end of #footer-area -->
    </footer>

</div><!-- #wrapper -->
<script type="text/javascript"
        src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
% if hasattr(self,'js'):
    ${self.js()}
% endif
<!-- Free template created by http://freehtml5templates.com -->
</body>
</html>