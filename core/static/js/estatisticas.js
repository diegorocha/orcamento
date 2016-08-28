$(document).ready(function(){

    function drawChart(data, i){
        var chart_div = "chart_div_" + i
        var chart_div_selector = '#' + chart_div;
        $('#chart_div').append('<div id="' + chart_div + '" class="grafico_estatistica"></div>');
        chart_data = [];
        data.categorias.forEach(function(categoria){
            chart_data.push({name: categoria.categoria, y: categoria.total});
        });
        $(chart_div_selector).highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Estatísticas de ' +  data.orcamento,
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            series: [{
                name: 'Categorias',
                colorByPoint: true,
                data: chart_data,
            }]
        });
    }

    function loadChart(){
        $.ajax({
            url: "/api/orcamento/estatisticas/",
        }).success(function(data){
            $('#chart_div').html("");
            for(i=0; data.length; i++){
                drawChart(data[i], i);
            }
        })
    }

    loadChart();
});
