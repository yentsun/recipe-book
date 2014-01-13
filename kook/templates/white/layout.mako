<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>${self.title()} - recipe-book.info</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/white/css/main.css" rel="stylesheet">
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    % if hasattr(self,'css'):
        ${self.css()}
    % endif
    <link rel="shortcut icon" href="/static/img/favicon.ico">
    <meta name="google-site-verification"
          content="PR3r5tN0wrf2I5XMNQRe-zWz7nIzTMllhVclofp0g38" />
</head>

<body
    % if hasattr(self,'body_id'):
    id="${self.body_id()}"
    % endif
>
<div id="wrapper">
    <header>
        <img src="/static/img/logo.png" width="300" height="73" alt="логотип"/>
        <nav class="pull-right">
            <a href="/about">О проекте</a> |
            <a href="/categories">Рецепты</a> |
            <a class="last" href="/reg">Регистрация</a>
        </nav>
    </header>
    <div id="content">
    ${next.body()}
    </div>
    <footer>
        <div id="email">
            email:
            <a href="mailto:general@recipe-book.info">
                general@recipe-book.info
            </a>
        </div>
        <div id="info">
            Все права защищены &copy; 2013
        </div>

    </footer>
</div>
<script type="text/javascript"
        src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
<script src="/static/bootstrap/js/bootstrap.min.js"></script>
##<script src="/static/white/js/main.js"></script>
    % if hasattr(self,'js'):
        ${self.js()}
    % endif
</body>
</html>