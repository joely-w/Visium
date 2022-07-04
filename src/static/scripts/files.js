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
        url: '/upload',
        type: 'post',
        xhr: function () {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    const percentComplete = ((evt.loaded / evt.total) * 100);
                    updateProgress(Math.round(percentComplete))
                }
            }, false);
            return xhr;
        },
        data: fd,
        contentType: false,
        processData: false,
        success: function (response) {
            window.location.href = '/browse.html'
        }
    });
}

function updateProgress(val) {
    const progress = $("#progress");
    progress.val(val)
    progress.width(`${val}%`)
    progress.html(`${val}%`)
}

$(document).ready(() => {
    $("#uploader").submit((e) => {
        e.preventDefault();
        uploadFile();
    })
})