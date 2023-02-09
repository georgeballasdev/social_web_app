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
                window.location.reload();
            }
            $(e.target).text(response.state);
        }
    });
})

// Scroll up button
const content = $('#content');
const profileInfo = $('#profile-info');
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
        scrollTop: $(profileInfo).offset().top
    }, 800, 'swing');
})