$(function(){
    $('#steps tr').click(function(){
        $(this).find('.no .btn').button('toggle');
        $(this).find('.icon-ok').toggle();
    });
    $('.btn').tooltip({placement: 'right'});
});

function vote(value, recipe_id, button) {
    $.post('/recipe_vote', {vote_value: value, recipe_id: recipe_id},
        function(data){
            if (data.status == 'error') {
                $(button).tooltip({title: data.message,
                                   placement: 'right'});
                $(button).tooltip('show');

            } else {
                $('#rating_value').text(data.new_rating);
                press($(button), value);
                unpress($(button).siblings('button'));
            }
        });
}

function unpress(button) {
    $(button).attr('data-original-title', 'Вы сможете проголосовать позже')
        .removeClass('active btn-success btn-warning')
        .find('i').removeClass('icon-white');
}

function press(button, value) {
    var btn_class = 'btn-success';
    if (value==-1) {
        btn_class = 'btn-warning';
        $(button).attr('data-original-title', 'Вы уже проголосовали -1');
    }
    else {
        $(button).find('i').addClass('icon-white');
        $(button).attr('data-original-title', 'Вы уже проголосовали +1');
    }
    $(button).addClass('active '+btn_class);
}

function post_comment(recipe_id) {
    var comment_text = $('#comment_text').val();
    $.post('/post_comment', {comment_text: comment_text, recipe_id: recipe_id},
           function(data){
               if (data !== '') {
                   var new_post_html = $(data);
                   new_post_html.appendTo('#comment_list').hide().fadeIn();
               }
           });
}

function delete_comment(cont, recipe_id, creation_time) {
    var confirm_delete = confirm('Действительно удалить комментарий?');
    if (confirm_delete) {
        $.get('/delete_comment/'+recipe_id+'/'+creation_time, function(data){
            if (data.status=='ok')
                $(cont).parents('.item').fadeOut();
        });
    }
}

function update_comment() {
    $('#comments .item .text').editable(function(value, settings) {
        console.log(this);
        console.log(value);
        console.log(settings);
        return(value);
    }, {
        type    : 'textarea',
        submit  : 'OK'
    });
}