<%inherit file="../layout.mako"/>
<%def name="body_id()">tag</%def>
<%def name="title()">${tag.title}</%def>
<div class="page-header">
    <h1 class="tag-title"> ${self.title()}
        % if hasattr(self,'sub_title'):
                <small>${self.sub_title()}</small>
        % endif
    </h1>
    % if hasattr(self,'additional_buttons'):
        ${self.additional_buttons()}
    % endif
</div>
<div class="row">
    <div class="span12">
        <ul class="thumbnails">
            % for dish in dishes:
            <li class="span3" title="${dish.title}">
                <a href="${request.route_path('read_dish', title=dish.title)}"
                   class="thumbnail">
                    <div class="img"
                         style="background-image:url(${dish.image.url})">
                         <span class="badge" title="Всего рецептов блюда">
                            ${len(dish.recipes)}
                         </span>
                    </div>
                    <div class="caption">
                        <h4>${dish.title}</h4>
                    </div>
                </a>
            </li>
            % endfor
        </ul>
    </div>
</div>
<%def name="js()">
    <script type="text/javascript"
            src="/static/bootstrap/js/bootstrap-button.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/read_recipe.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/jquery.jeditable.mini.js"></script>
    <script type="text/javascript"
            src="/static/bootstrap/js/tag.js"></script>
</%def>
% if request.user:
<script type="text/javascript">
    var user = ${request.user.to_json() | n};
</script>
% endif