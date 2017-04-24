$(document).ready(function(){

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
    });

    $('form').submit(function(e){
        e.preventDefault();
        data = {};
        data['fatura'] = parseInt($('#fatura').val());
        data['descricao'] = $('#descricao').val();
        data['descricao_fatura'] = $('#descricao_fatura').val();
        data['valor_real'] = parseFloat($('#valor_real').val());
        var valor_dolar = $('#valor_dolar').val();
        if(valor_dolar != undefined && valor_dolar != ""){
            data['valor_dolar'] = parseFloat(valor_dolar);
        }
        data['categoria'] = parseInt($('#categoria').val());
        data['parcelas'] = parseInt($('#parcelas').val());
        data['parcela_atual'] = 1;
        var recorrente = $('#recorrente').val();
        if(recorrente != undefined && recorrente != "") {
            data['recorrente'] = parseInt(recorrente);
        }else{
            data['recorrente'] = 0;
        }
        console.log(data);
        $.ajax({
             url: "/api/cartao/compra/",
             type : "POST",
             data: data,
             success: function() {
                 $('#sucesso').show().delay(5000).fadeOut();
             },
             error: function(xhr, status, error){
                 console.log(xhr, status, error);
                 $('#erro').show().delay(5000).fadeOut();
             }
        });
    });

});