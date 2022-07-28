const checked = {}

function loadPdf(project_name, filepath) {
    $("#hist").html(`<embed src="/api/directory/${project_name}/pdf?filename=${filepath}" type="application/pdf" width="100%" height="100%" />`)
    $("#graph").show()
}


function resetSearch() {
    $("#search").val(null)
    $("#tree").jstree('clear_search');
    $("#reset_btn").hide();
}

$(document).ready(() => {
    const filetree = $("#file-tree")


    $('#tree').on("select_node.jstree", function (e, data) {
        const path = data.node.id;
        const splits = path.split('.');
        const ext = splits[splits.length - 1];
        const project_name = $("#files").val()
        const full_path = project_name + '/' + path;
        filetree.hide();

        switch (ext) {
            case "yaml":
                loadAll('histogram', full_path);
                break;
            case "txt":
                loadAll('correlation_matrix', full_path);
                break;
            case "pdf":
                loadPdf(project_name, path)
        }
    });
    $("#search_btn").click(function () {
        const search = $("#search").val();
        if (!search.trim()) {
            resetSearch();
        }
        $("#reset_btn").show()
        $("#tree").jstree("search", search.trim());
    })
    $("#reset_btn").click(function () {
        resetSearch();
    })
    $.get("/api/browse", response => {
        for (let i = 0; i < response.result.length; i++) {
            $("#files").append(`<option>${response.result[i]}</option>`)
        }
    });
    $("#files").change(() => {
        $.get(`/api/directory/${$("#files").val()}`, response => {
            response = JSON.parse(response)
            $("#file-tree").show();
            $("#select").hide()
            const tree = $('#tree').jstree({
                plugins: ["types", "sort", "search", "checkbox"], core: {
                    data: response.children
                }, search: {
                    show_only_matches: true, case_insensitive: true,
                }, checkbox: {
                    three_state: false, // to avoid that fact that checking a node also check others
                    whole_node: false,  // to avoid checking the box just clicking the node
                    tie_selection: false // for checking without selecting and selecting without checking
                }, sort: function (a, b) {
                    let a1 = this.get_node(a);
                    let b1 = this.get_node(b);
                    if (a1.icon === b1.icon) {
                        return (a1.text > b1.text) ? 1 : -1;
                    } else {
                        return (a1.icon === 'folder') ? 1 : -1
                    }
                }, types: {
                    file: {
                        icon: "fa fa-file text-warning"
                    }, folder: {
                        icon: "fa fa-folder"
                    }
                },
            });
            tree.on("check_node.jstree uncheck_node.jstree", function (e, data) {
                if (!data.node.state.checked) {
                    delete checked[data.node.id];
                } else {
                    checked[data.node.id] = true
                }
                const len = Object.keys(checked).length
                if (len === 2) {
                    $("#compare_btn").show();
                    // Show compare
                } else {
                    $("#compare_btn").hide();
                    // Hide compare
                }
            })
        })
    });
    $("#back").click(() => {
        $("#graph").hide()
        $("#hist").html(null)
        $("#file-tree").show()
    })
    $("#compare_btn").click(() => {
        filetree.hide()
        loadComparison($("#files").val(), ...Object.keys(checked))
    })
})

function resetHeaders() {
    $("#nuis").val(null)
    data = JSON.parse(JSON.stringify(original_data))
    Plotly.newPlot($("#hist")[0], data)

}

function displayHeaders() {
    const search = $("#nuis").val().trim()
    const regex = new RegExp(search)
    let [error, error_minus, vals, index] = [[], [], [], []]
    let [err, err_min, vals_1, index_1] = [[], [], [], []]
    for (let i = 0; i < original_data.data[0].x.length; i++) {
        if (original_data.data[0].y[i].includes(search) || original_data.data[0].y[i].match(regex)) {
            vals.push(original_data.data[0].y[i])
            index.push(original_data.data[0].x[i])
            error.push(original_data.data[0]['error_x'].array[i])
            error_minus.push(original_data.data[0]['error_x'].arrayminus[i])
        }
    }
    for (let i = 0; i < original_data.data[1].x.length; i++) {
        if (original_data.data[1].y[i].includes(search) || original_data.data[1].y[i].match(regex)) {
            vals_1.push(original_data.data[1].y[i])
            index_1.push(original_data.data[1].x[i])
            err.push(original_data.data[1]['error_x'].array[i])
            err_min.push(original_data.data[1]['error_x'].arrayminus[i])
        }
    }
    data.data[0].x = index;
    data.data[0].y = vals;
    data.data[0]['error_x'].array = error;
    data.data[0]['error_x'].arrayminus = error_minus;
    data.data[1].x = index_1;
    data.data[1].y = vals_1;
    data.data[1]['error_x'].array = err;
    data.data[1]['error_x'].arrayminus = err_min;
    Plotly.redraw($("#hist")[0])
}