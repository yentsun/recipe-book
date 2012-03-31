<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${self.title()} - база рецептов "Kook"</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/bootstrap/css/main.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    % if hasattr(self,'css'):
      ${self.css()}
    % endif

    <link rel="shortcut icon" href="/static/img/favicon.png">
  </head>

  <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="/">Kook</a>
          <div class="nav-collapse">
            <ul class="nav">
              <li class="active"><a href="/">Главная</a></li>
              <li><a href="#about">Все рецепты</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
      <div class="page-header"><h1>${self.title()}
          % if hasattr(self,'sub_title'):
          <small>${self.sub_title()}</small>
          % endif
      </h1></div>
      ${next.body()}
    </div> <!-- /container -->

    <script type="text/javascript"
            src="http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
    % if hasattr(self,'js'):
    ${self.js()}
    % endif
  </body>
</html>
