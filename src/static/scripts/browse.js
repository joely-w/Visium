const cmp = function (a, b) {

    const x = (a.data.isFolder ? "0" : "1") + a.data.title.toLowerCase(),
        y = (b.data.isFolder ? "0" : "1") + b.data.title.toLowerCase();
    return x === y ? 0 : x > y ? 1 : -1;
};
$(document).ready(() => {
    $.get("/api/browse", response => {
        for (let i = 0; i < response.result.length; i++) {
            $("#files").append(`<option>${response.result[i]}</option>`)
        }
    });
    $("#files").change(() => {
        $.get(`/api/directory/${$("#files").val()}`, response => {
            response = JSON.parse(response)
            console.log(response)
            const tree = $("#tree").fancytree({
                extensions: ["edit", "filter"],
                source: response.children,
                click: (event, data) => {
                    const path = data.node.data['rootpath']
                    const filename = path[path.length - 1]
                    if (filename.substring(filename.length - 5) === '.yaml') {
                        $("#tree").hide()
                        loadAll($("#files").val() + '/' + path.join('/'))
                    }
                }
            });
        })
    });
    $("#back").click(() => {
        $("#graph").hide()
        $("#tree").show()
    })
})
