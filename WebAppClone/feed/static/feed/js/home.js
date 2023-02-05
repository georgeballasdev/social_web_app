const feed = $('#posts');
const content = $('#content');

content.on('scroll', (e) => {
    if (e.target.offsetHeight + e.target.scrollTop >= e.target.scrollHeight) {
        $.ajax({
            type: 'POST',
            url: DATASET.nextPosts,
            data:
            {
                iteration: feed.attr('data-iteration'),
                csrfmiddlewaretoken: DATASET.token
            },
            success: (response) => {
                posts = response['posts'];
                for (var i = 0; i < posts.length; i++) {
                    feed.append(loadPost(posts[i]));
                }
                feed.attr('data-iteration', parseInt(feed.attr('data-iteration')) + 1);
            }
        });
    }
})

function loadPost(data) {
    let post = $('<div/>',{
        class: 'post',
        id: data['id']
    });

    let postHeader = $('<div/>',{
        class: 'post-header'
    });
    let postTimestamp = $('<span/>',{
        class: 'post-timestamp',
        text: data['timestamp']
    });
    let postTitle = $('<div/>',{
        class: 'post-title'
    });
    postTitle.append('<img class="pic" src="' + data['pic'] + '" alt="pic">\
               <span>\
                   <a href="' + data['post_url'] + '">Post</a> by\
                   <a href="' + data['profile_url'] + '"> ' + data['owner'] + '</a>\
               </span>'
    );
    let likeBtn;
    if (data['liked']) {
        likeBtn = '<i data-like-command="unlike" class="like-btn fa-solid fa-heart hoverable"></i>'
    }
    else {
        likeBtn = '<i data-like-command="like" class="like-btn fa-regular fa-heart hoverable"></i>'
    }
    let postLikes = $('<div/>',{
        class: 'post-likes'
    });
    postLikes.append('<div class="likes-count">' +
            data['likes'] + ' likes</div>' +
            likeBtn
    );
    postHeader.append(postTimestamp);
    postHeader.append(postTitle);
    postHeader.append(postLikes);

    let postImg;
    if (data['img'] != '') {
        postImg = '<img class="post-img" src="' + data['img'] + '" alt="image">';
    }
    else {
        postImg = '';
    }
    let postContent = $('<div/>',{
        class: 'post-content'
    });
    postContent.append(postImg +
              '<div class="post-body">'
              + data['text'] + '</div>'
    );

    let postComments = $('<div/>',{
        class: 'post-comments'
    });
    let comments = $('<div/>',{
        class: 'comments'
    });
    for (var i = 0; i < data['comments'].length; i++) {
        let comment = data['comments'][i];
        comments.append(
            '<div class="comment">\
                <img class="pic" alt="pic" src="' + comment['pic']+ '">\
                <span class="comment-user"><a href="' + comment['profile_url'] + '">' + comment['user'] + ':</a> </span>\
                <span class="comment-text">' + comment['text'] + '</span>\
                <span class="comment-timestamp">' + comment['timestamp'] + '</span>\
            </div>'
        );
    }
    postComments.append('<span>Comments:</span>');
    postComments.append(comments);
    let postForm = $('<form/>',{
        class: 'add-comment'
    });
    postForm.append(
        '<input type="text">\
        <input type="submit" value="ADD COMMENT" class="hoverable">'
    );
    postComments.append(postForm);

    post.append(postHeader);
    post.append(postContent);
    post.append(postComments);
    return post;
}