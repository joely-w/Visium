const cmp = function (a, b) {

    if (a.data.folder === b.data.folder) {
        return (a.data.id > b.data.id) ? 1 : -1;
    } else {
        return (a.data.folder > b.data.folder) ? 1 : -1;
    }
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
            $('#tree').jstree({
                plugins: ["types", "sort"],
                core: {
                    data: response.children
                },
                'sort': function (a, b) {
                    a1 = this.get_node(a);
                    b1 = this.get_node(b);
                    if (a1.icon === b1.icon) {
                        return (a1.text > b1.text) ? 1 : -1;
                    } else {
                        return (a1.icon === 'folder') ? 1 : -1
                    }
                },
                types: {
                    file: {
                        icon: "fa fa-file  text-warning"
                    },
                    folder: {
                        icon: "fa fa-folder text-warning"
                    }
                },
            });

        })
    });
    $("#back").click(() => {
        $("#graph").hide()
        $("#tree").show()
    })
})
