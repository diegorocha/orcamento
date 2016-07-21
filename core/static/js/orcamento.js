$(document).ready(function(){

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
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

    $('.save').hide();
    $('.cancel').hide();
    $('table input').hide();

    $('.edit').on('click', function(){
        var td = $(this).parent();
        var tr = td.parent();
        td.find('.save').show();
        td.find('.cancel').show();
        td.find('.edit').hide();
        td.find('.delete').hide();
        tr.find('input').show();
        tr.find('.text').hide();
    });

    $('.cancel').on('click', function(){
        var td = $(this).parent();
        var tr = td.parent();
        td.find('.save').hide();
        td.find('.cancel').hide();
        td.find('.edit').show();
        td.find('.delete').show();
        tr.find('input').hide();
        tr.find('.text').show();
    });

    $('.save').on('click', function(){
        var td = $(this).parent();
        var tr = td.parent();
        td.find('.save').hide();
        td.find('.cancel').hide();
        td.find('.edit').show();
        td.find('.delete').show();
        tr.find('input').hide();
        tr.find('.text').show();
        var endpoint = "/api/conta/" + tr.attr('data-id') + "/";
        var dados = {};
        dados['nome'] = tr.find('input.nome').val();
        dados['descricao'] = tr.find('input.descricao').val();
        dados['previsto'] = tr.find('input.previsto').val();
        dados['atual'] = tr.find('input.atual').val();
        dados['pago'] = tr.find('input.pago').val();

        console.log(dados);
        $.ajax({
            url: endpoint,
            type : "PATCH",
            data: dados,
            success: function(result) {
                console.log(result);
                tr.find('.text.nome').html(result.nome);
                tr.find('.text.descricao').html(result.descricao);
                tr.find('.text.previsto').html(result.previsto);
                tr.find('.text.atual').html(result.atual);
                tr.find('.text.pago').html(result.pago);
            }
        });
    });


});
