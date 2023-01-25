$(".like-btn").on('click', function(e) {
    e.preventDefault();
    let post_id = $(this).closest('.post').attr('post-id');
    $.ajax({
        type: 'POST',
        url: likes_url,
        data:
        {
            post_id: post_id,
            command: $(this).text(),
            csrfmiddlewaretoken: token
        },
        success: (response) => {
            $(this).text(response["command"]);
            $(this).prev().text(response["likes_count"] + ' likes');
        }
    });
})

$(".add-comment").on('submit', function(e) {
    e.preventDefault();
    let post_id = $(this).closest('.post').attr('post-id');
    let text_input = $(this).find('input[type=text]');
    let comments_section = $(this).prev();
    $.ajax({
        type: 'POST',
        url: comments_url,
        data:
        {
            post_id: post_id,
            comment: text_input.val(),
            csrfmiddlewaretoken: token
        },
        success: (response) => {
            text_input.val('');
            comments = response['comments'];
            comments_section.empty();
            for (var i = 0; i < comments.length; i++){
                comments_section.append('<div class="comment">'+
                                    '<span class="comment-user">'+
                                    comments[i][0]+'</span>'+
                                    comments[i][1]+' - '+comments[i][2]+
                                '</div>');
            }
            comments_section.scrollTop(9999);
        }
    });
})