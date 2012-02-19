## -*- coding: utf-8 -*-
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<title>${self.title()} - база рецептов</title>
		<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
  		<meta name="keywords" content="рецепт, сборник рецептов, кулинарная книга">
  		<meta name="description" content="база кулинарных рецептов">
		<link rel="shortcut icon" href="/static/favicon.png">
		<link rel="stylesheet" href="/static/css/main.css" type="text/css" media="screen" charset="utf-8">
        % if hasattr(self,'css'):
		${self.css()}
		% endif
	</head>
	<body>
        <div id="header">
            <img width="108" height="150" id="logo" src="/static/img/logo.png" alt="Логотип">
            <h1>
                база кулинарных рецептов
            </h1>
        </div>
        <div id="middle">
            <div id="nav">
                <%
                    nav = {
                        u'список рецептов': '/',
                        u'добавить рецепт': request.route_url('create_recipe')
                          }
                %>
                % for item in nav:
                    % if nav[item] == request.path:
                        <span class="${item}">${item}</span>
                    % else:
                        <a class="${item}" href="${nav[item]}">${item}</a>
                    % endif
                % endfor
            </div>
            <div id="wrapper">
                ${next.body()}
            </div>
    </div>
    <div id="footer">
        <div id="copy">&copy; 2011</div>
    </div>
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
		% if hasattr(self,'js'):
		${self.js()}
		% endif
	</body>
</html>