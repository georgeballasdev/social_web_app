$('#friendship-btn').click( (e) => {
    e.preventDefault();
    let btn = $('#btn-state');
    $.ajax({
        type: 'POST',
        url: handleurl,
        data:
        {
        command: btn.val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: (response) => {
            btn.val(response['state']);
        }
    });
})