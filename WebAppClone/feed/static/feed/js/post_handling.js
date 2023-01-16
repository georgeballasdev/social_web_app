// FUNCTIONS
function updateComments(id) {
url = get_comments_url;
$.getJSON(url, {id:id}, function(comments) {
    $('#comments_of_'+id).empty();
    for (var i = 0; i < comments.length; i++) {
    x = comments[i];
    $('#comments_of_'+id).append('<p>'+x[0]+':'+x[1]+'</p>\n');
    }
})
};

function updateLikes(id) {
url = get_likes_url + id;
$.getJSON(url, function(n) {
    $('#likes_of_'+id).text(n);
})
};

// EVENTS

// Like button clicked
$("form[id^='like_btn_']").on('click', function(e) {
post_id = $(this).attr('id').slice(9,);
e.preventDefault();
$.ajax({
    type: 'POST',
    url: like_url,
    data:
    {
    id: post_id,
    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    }
});
updateLikes(post_id);
$('#unlike_btn_'+post_id).toggle();
$(this).toggle();
});

// Unlike button clicked
$("form[id^='unlike_btn_']").on('click', function(e) {
post_id = $(this).attr('id').slice(11,);
e.preventDefault();
$.ajax({
    type: 'POST',
    url: unlike_url,
    data:
    {
    id: post_id,
    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    }
});
updateLikes(post_id);
$('#like_btn_'+post_id).toggle();
$(this).toggle();
});

$("form[id^='add_comment_to']").submit(function(e) {
post_id = $(this).attr('id').slice(15,);
comment = $(this).children("input:last").val();
e.preventDefault();
$.ajax({
    type: 'POST',
    url: add_comment_url,
    data:
    {
    id: post_id,
    text: comment,
    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    }
});
$(this).children("input:last").val('');
updateComments(post_id);
});