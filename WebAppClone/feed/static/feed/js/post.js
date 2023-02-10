// Handle post like
$('#content').on('click', '.like-btn', (e) => {
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

// Handle post comment submit
$('#content').on('submit', '.add-comment', (e) => {
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
            let comment = response['comment'];
            if (comments[0].firstElementChild.classList.contains('placeholder')) {
                comments.empty();
            }
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