$(document).ready(function(){

    function drawChartMercado(data){
        var total = {'name': 'Total', 'data': []};
        data.data.forEach(function(serie, i){
            var min = serie.data[0];
            var max = serie.data[0];
            var soma = 0;
            serie.data.forEach(function(value, index){
                var sum = total.data[index] || 0;
                sum += value;
                if(value < min){
                    min = value;
                }
                if(value > max){
                    max = value;
                }
                soma += value;
                total.data[index] = parseFloat(sum.toFixed(2));
            });
            $('#avg_'+ i +'_min').html(min.toFixed(2));
            $('#avg_'+ i +'_med').html((soma / serie.data.length).toFixed(2));
            $('#avg_'+ i +'_max').html(max.toFixed(2));
        });
        var total_min = total.data[0];
        var total_max = total.data[0];
        var total_soma = 0;
        total.data.forEach(function(value){
            if(value < total_min){
                total_min = value;
            }
            if(value > total_max){
                total_max = value;
            }
            total_soma += value;
        });
        $('#avg_2_min').html(total_min.toFixed(2));
        $('#avg_2_med').html((total_soma / total.data.length).toFixed(2));
        $('#avg_2_max').html(total_max.toFixed(2));
        data.data.push(total);
        $('#chart_div_mercado').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Gastos com Mercado'
            },
            xAxis: {
                categories: data.eixos,
            },
            yAxis: {
                title: {
                    text: 'R$'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                }
            },
            series: data.data,
        });
        $('#table_mercado').show();
    }

    function drawChartTotal(data){
        $('#chart_div_total').highcharts({
            chart: {
                type: 'line'
            },
            title: {
                text: 'Total Orçamento'
            },
            xAxis: {
                categories: data.eixos,
            },
            yAxis: {
                title: {
                    text: 'R$'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                }
            },
            series: data.data,
        });
    }

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

    function loadChartMercado(){
        $.ajax({
            url: "/api/orcamento/mercado/",
        }).success(function(data){
            drawChartMercado(data);
        });
    }

    function loadChartTotal(){
        $.ajax({
            url: "/api/orcamento/total/",
        }).success(function(data){
            drawChartTotal(data);
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
    loadChartMercado();
    loadChartTotal();
});
