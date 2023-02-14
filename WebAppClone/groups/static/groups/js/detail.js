// Handle join button
$('#join-btn').click( (e) => {
    $.ajax({
        type: 'POST',
        url: GROUP_DATASET.handleMembershipUrl,
        data:
        {
        command: $(e.target).text(),
        csrfmiddlewaretoken: DATASET.token
        },
        success: (response) => {
            if (response.state == 'REFRESH') {
                updateInfoMessage('Left group');
                window.location.reload();
            }
            else {
                $(e.target).text(response.state);
            }
        }
    });
})

// Scroll up button
const content = $('#content');
const groupInfo = $('#group-info');
const scrollHomeBtn = $('#scroll-home');

content.on('scroll', (e) => {
    if (e.target.scrollTop > 250) {
        scrollHomeBtn.show();
    }
    else {
        scrollHomeBtn.hide();
    }
})

scrollHomeBtn.on('click', (e) => {
    e.preventDefault();
    content.animate({
        scrollTop: $(groupInfo).offset().top
    }, 800, 'swing');
})