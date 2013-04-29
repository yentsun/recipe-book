<%!
    from pyramid.security import has_permission
%>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>${self.title()} - база рецептов "Kook"</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/bootstrap/css/bootstrap-responsive.min.css"
          rel="stylesheet">
    <link href="/static/bootstrap/css/main.css" rel="stylesheet">
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    % if hasattr(self,'css'):
        ${self.css()}
    % endif
    <link rel="shortcut icon" href="/static/img/favicon.png">
    <meta name="google-site-verification"
          content="PR3r5tN0wrf2I5XMNQRe-zWz7nIzTMllhVclofp0g38" />
</head>

<body
    % if hasattr(self,'body_id'):
    id="${self.body_id()}"
    % endif
>
<div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
        <div class="container">
            <a class="btn btn-navbar" data-toggle="collapse"
               data-target=".nav-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </a>
            <a class="brand" href="/">Kook</a>
            <div class="nav-collapse">
                <ul class="nav">
                    <li class="active"><a href="/">Главная</a></li>
                    % if request.user:
                    <li>
                        <a href="${request.route_path('dashboard')}">
                            Моя страница
                        </a>
                    </li>
                        % if has_permission('manage_dishes', request.root, request):
                    <li>
                        <a href="${request.route_path('dishes')}">
                            Блюда
                        </a>
                    </li>
                        % endif
                        % if has_permission('manage_products', request.root, request):
                    <li>
                        <a href="${request.route_path('products')}">
                            Продукты и меры
                        </a>
                    </li>
                         % endif
                    % endif
                </ul>
                <ul class="nav pull-right">
                        % if request.user:
                        <li><a href="${request.route_path('update_profile')}">
                            <img width=20 src="${request.user.gravatar_url()}"
                                 alt="gravatar" height="20">
                            % if request.user.profile.nickname:
                            ${request.user.profile.nickname}
                            % elif request.user.profile.real_name:
                            ${request.user.profile.real_name}
                            % else:
                            ${request.user.email}
                            % endif
                            <strong>
                                ${request.user.profile.rep}
                            </strong>
                        </a></li>
                        <li><a href="${request.route_path('logout')}">
                            <i class="icon-share icon-white"></i>
                            выйти
                        </a></li>
                        % else:
                        <li><a href="${request.route_path('login')}">
                            <i class="icon-chevron-right icon-white"></i>
                            войти
                        </a></li>
                        % endif
                </ul>
            </div><!--/.nav-collapse -->
        </div>
    </div>
</div>
<div id="main" class="container-fluid">
    ${next.body()}
</div> <!-- /container -->
<script type="text/javascript"
        src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
<script src="/static/bootstrap/js/bootstrap.min.js"></script>
<script src="/static/bootstrap/js/main.js"></script>
    % if hasattr(self,'js'):
        ${self.js()}
    % endif
</body>
</html>