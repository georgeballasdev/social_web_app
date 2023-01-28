$('#friendship-btn').click( (e) => {
    e.preventDefault();
    let btn = $('#btn-state');
    $.ajax({
        type: 'POST',
        url: PROFILE_DATASET.handleUrl,
        data:
        {
        command: btn.val(),
        csrfmiddlewaretoken: DATASET.token
        },
        success: (response) => {
            btn.val(response['state']);
        }
    });
})