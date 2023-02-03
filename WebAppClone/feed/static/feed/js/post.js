$(".like-btn").on('click', (e) => {
    e.preventDefault();
    let post_id = $(e.target).closest('.post').attr('id');
    $.ajax({
        type: 'POST',
        url: DATASET.likesUrl,
        data:
        {
            post_id: post_id,
            command: e.target.dataset.likeCommand,
            csrfmiddlewaretoken: DATASET.token
        },
        success: (response) => {
            $(e.target).toggleClass('fa-solid');
            $(e.target).toggleClass('fa-regular');
            $(e.target).attr('data-like-command', response['command']);
            $(e.target).prev().text(response["likes_count"] + ' likes');
        }
    });
})

$(".add-comment").on('submit', (e) => {
    e.preventDefault();
    let postId = $(e.target).closest('.post').attr('id');
    let textInput = $(e.target).find('input[type=text]');
    let comments = $(e.target).prev();
    $.ajax({
        type: 'POST',
        url: DATASET.commentsUrl,
        data:
        {
            post_id: postId,
            comment: textInput.val(),
            csrfmiddlewaretoken: DATASET.token
        },
        success: (response) => {
            textInput.val('');
            comment = response['comment'];
            comments.append(
                '<div class="comment">\
                    <img class="pic" src="' + comment.url + '" alt="pic">\
                    <span class="comment-user"><a href="' + comment.profile + '">' + comment.user + ':</a> </span>\
                    <span class="comment-text">' + comment.text + '</span>\
                    <span class="comment-timestamp">' + comment.timestamp + '</span>\
                </div>');
            comments.scrollTop(9999);
        }
    });
})