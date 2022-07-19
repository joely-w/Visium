/**
 * Load all graphs onto chart
 */
function loadAll(type, filepath) {
    $.ajax({
        url: `/api/${type}`,
        type: "POST",
        data: JSON.stringify(filepath),
        contentType: 'application/json; charset=utf-8',
        success: (response) => {
            $("#hist").html(null)
            Plotly.newPlot($("#hist")[0], response)
            $("#graph").show()
        },
        error: (message) => {
            $("#hist").html(message.responseText)
            $("#graph").show()
        }
    })
}

function loadComparison(project, path1, path2) {
    $.ajax({
        url: "/api/comparison",
        type: "post",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({project, path1, path2}),
        success: (response) => {
            $("#hist").html(null)
            $("#info").html(`Top left:${path1}<br> Bottom right: ${path2}<br>`)
            Plotly.newPlot($("#hist")[0], response)
            $("#graph").show()
        },
        error: (message) => {
            $("#hist").html(message.responseText)
            $("#graph").show()
        }
    });

}
