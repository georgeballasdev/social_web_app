$('#content').on('click', '.handle-btn', (e) => {
    let memberId = $(e.target).data().memberId;
    $.ajax({
        type: 'POST',
        url: GROUP_DATASET.handleMemberUrl,
        data:
        {
            command: $(e.target).text(),
            id: memberId,
            csrfmiddlewaretoken: DATASET.token
        },
        success: (response) => {
            let state = response.state;
            $(e.target).closest('.member').append('<span class="state">' + state + '</span');
            $('.handle-btn[data-member-id="' + memberId + '"]').remove();
            $(e.target).remove();
        }
    });
})