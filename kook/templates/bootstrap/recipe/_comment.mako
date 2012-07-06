<%page args="comment, can_edit"/>
<div class="item">
    <span class="text">${comment.markdown_text | n}</span> —
    <span class="sig">
         <span class="time">
             ${comment.pretty_time}
         </span>
         <a class="author" href="/">
             ${comment.author.display_name}
         </a>
        % if can_edit:
        <a title="редактировать" class="icon icon-pencil" href=""></a>
        <a title="удалить" class="icon icon-remove"
           onclick="delete_comment(this, '${comment.recipe.id}',
                                   '${comment.creation_time}')"></a>
        % endif
    </span>
</div>