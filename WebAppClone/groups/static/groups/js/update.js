const imgInput = document.querySelector('#id_img');
const preview = document.querySelector('#preview');

imgInput.onchange = () => {
    const [file] = imgInput.files
    if (file) {
        preview.src = URL.createObjectURL(file);
    }  
}

$('#delete').on('click', () => {
    $.confirm({
        boxWidth: '40%',
        useBootstrap: false,
        title: GROUP_DATASET.group,
        content: 'Delete this group?',
        buttons: {
            delete: () => {
                $.ajax({     
                    url: GROUP_DATASET.deleteUrl,
                    type: 'POST',
                    data: {csrfmiddlewaretoken: DATASET.token},
                    success: () => {
                        window.location.href = window.location.origin;
                    }
                });
            },
            cancel: () => {}
        },
    });
})