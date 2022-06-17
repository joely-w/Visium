const reader = new FileReader();
reader.addEventListener('load', (event) => {
    const data = jsyaml.load(event.target.result);
    loadAll(data);
})

function submit() {
    const file = $("#file-selector")[0].files[0];
    reader.readAsText(file)
}

/**
 * Load all graphs onto chart
 */
function loadAll(content) {
    console.log(content)
    $.ajax({
        url: '/figure',
        type: "POST",
        data: JSON.stringify(content),
        contentType: 'application/json;',
        success: (response) => {
            $("#reupload").show()
            $(".upload").hide()
            Plotly.newPlot($("#hist")[0], response)
        }
    })
}
