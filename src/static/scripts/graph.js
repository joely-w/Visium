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
            $("#hist").html(null)
            Plotly.newPlot($("#hist")[0], response)
            $("#graph").show()
        },
        error: (message) => {
            $("#hist").html(message.responseText)
        }
    })
}
