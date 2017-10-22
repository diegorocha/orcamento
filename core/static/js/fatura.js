$(document).ready(function(){
    function loadGrafico(){
        var divGrafico = $('#grafico_estatistica');
        var estatistica = divGrafico.data('estatistica');
        dataEntries = Object.entries(estatistica);
        console.log(dataEntries);

        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Categoria');
        data.addColumn('number', 'Valor');
        data.addRows(dataEntries);

        var options = {'title': 'Gastos por categoria',
                       'width': '100%',
                       'height': 500};
        var chart = new google.visualization.PieChart(divGrafico[0]);
        chart.draw(data, options);

    }

    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(loadGrafico);

    $(window).on("throttledresize", function () {
        loadGrafico();
    });
});