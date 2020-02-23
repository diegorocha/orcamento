$(document).ready(function(){

    $('.btn-accordion').click(function(){
        const classShow = 'glyphicon-collapse-down';
        const classHide = 'glyphicon-collapse-up';
        const tabela = $(this).parent().parent().find('.gastos-dia-tabela');
        const icon = $(this).parent().find('.glyphicon');

        if(icon.hasClass(classShow)){
            icon.removeClass(classShow).addClass(classHide);
        }else{
            icon.removeClass(classHide).addClass(classShow);
        }

        if(tabela.hasClass('hidden')){
            tabela.removeClass('hidden');
        }else{
            tabela.addClass('hidden');
        }
    });


    const data = $('.categoria_total').map(function () {
        return {
            name: $(this).data('name'),
            y: parseFloat($(this).data('value').replace(',', '.'))
        }
    }).toArray();

    Highcharts.chart('grafico_categoria_viagem', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Gastos x Categoria'
        },
        tooltip: {
            pointFormat: '{point.name}: <b>{point.y} - {point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f}%'
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Categorias',
            colorByPoint: true,
            data: data
        }]
    });
});
