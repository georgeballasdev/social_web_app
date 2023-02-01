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
    let post_id = $(e.target).closest('.post').attr('id');
    let text_input = $(e.target).find('input[type=text]');
    let comments_section = $(e.target).prev();
    $.ajax({
        type: 'POST',
        url: DATASET.commentsUrl,
        data:
        {
            post_id: post_id,
            comment: text_input.val(),
            csrfmiddlewaretoken: DATASET.token
        },
        success: (response) => {
            text_input.val('');
            comment = response['comment'];
            comments_section.append(
                '<div class="comment">' +
                '<span class="comment-user">' +
                comment[0] + ': ' + '</span>' +
                comment[1] + ' - ' + comment[2] + '</div>');
            comments_section.scrollTop(9999);
        }
    });
})