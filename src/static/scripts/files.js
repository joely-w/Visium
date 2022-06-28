function uploadFile() {
    const fd = new FormData();
    const files = $('#file')[0].files;

    // Check file selected or not
    if (files.length > 0) {
        fd.append('file', files[0]);
    } else {
        return;
    }
    $.ajax({
        url: '/upload', type: 'post', data: fd, contentType: false, processData: false, success: function (response) {
            response = JSON.parse(response)
            $('#tree').jstree({
                'core': {
                    'data': [response]
                }
            });
        }
    });
}

$(document).ready(() => {
    $("#uploader").submit((e) => {
        e.preventDefault();
        uploadFile();
    })
})