document.getElementById('apply-filters').addEventListener('click', function(event) {
    event.preventDefault();

    const year = document.getElementById('year_filter').value;
    const quarter = document.getElementById('quarter_filter').value;
    const month = document.getElementById('month_filter').value;
    const developer = document.getElementById('developer_filter').value;

    fetch(`/chart-data/?year=${year}&quarter=${quarter}&month=${month}&developer=${developer}`)
        .then(response => response.json())
        .then(data => {
            const parsedData = JSON.parse(data);
            Plotly.newPlot('chart', parsedData.data, parsedData.layout);
        })
        .catch(error => console.error("Error updating chart:", error));
});

document.addEventListener("DOMContentLoaded", function () {
    const applyFiltersBtn = document.getElementById('apply_filters');
    const yearFilter = document.getElementById('year_filter');
    const quarterFilter = document.getElementById('quarter_filter');
    const monthFilter = document.getElementById('month_filter');
    const developerFilter = document.getElementById('developer_filter');

    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const year = yearFilter.value;
            const quarter = quarterFilter.value;
            const month = monthFilter.value;
            const developer = developerFilter.value;

            // Enviar datos al backend y actualizar la gráfica
            fetch(`/chart-data/?year=${year}&quarter=${quarter}&month=${month}&developer=${developer}`)
                .then(response => response.json())
                .then(data => {
                    const parsedData = JSON.parse(data);
                    Plotly.newPlot('chart', parsedData.data, parsedData.layout);
                })
                .catch(error => console.error("Error updating chart data:", error));
        });
    }
});

document.getElementById('ai-question-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const question = document.getElementById('ai_question').value;

    fetch(`/ask-ai/?question=${encodeURIComponent(question)}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('ai-response').innerText = data.response || 'No response from AI.';
        })
        .catch(error => console.error("Error asking AI:", error));
});

document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    const year = document.getElementById('year_filter').value;
    const quarter = document.getElementById('quarter_filter').value;
    const month = document.getElementById('month_filter').value;
    const developer = document.getElementById('developer_filter').value;

    fetch(`/chart-data/?year=${year}&quarter=${quarter}&month=${month}&developer=${developer}`)
        .then(response => response.json())
        .then(data => {
            const parsedData = JSON.parse(data);
            Plotly.newPlot('chart', parsedData.data, parsedData.layout);
        })
        .catch(error => console.error("Error loading chart data:", error));
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}