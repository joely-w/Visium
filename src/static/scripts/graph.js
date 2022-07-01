/**
 * Load all graphs onto chart
 */
function loadAll(filepath) {
    $.ajax({
        url: '/figure',
        type: "POST",
        data: JSON.stringify(filepath),
        contentType: 'application/json;',
        success: (response) => {
            $("#graph").show()
            Plotly.newPlot($("#hist")[0], response)
        },
        error: (message) => {
            $("#hist").html(message.responseText)
        }
    })
}
