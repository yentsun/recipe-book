<%inherit file="layout.mako"/>
<%def name="title()">${tag.title}</%def>
<%def name="js()"></%def>
<section id="tag">
    <hr>
    <h2>${tag.title}</h2>
    <ul class="thumbnails">
    % for dish in dishes:
        <%include file="_dish_preview.mako" args="dish=dish" />
    % endfor
    </ul>
</section>