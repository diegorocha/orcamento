$(document).ready(function(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            csrf_methods = ['POST', 'PUT', 'PATCH'];
            if(csrf_methods.indexOf(settings.type) > -1){
                xhr.setRequestHeader('X-CSRFToken', CRSF_TOKEN);
            }
        }
    });

    $('#refresh_categoria').click(function(e){
        e.preventDefault();
        $('#categoria').html('<option>Carregando...</option>');
        $.ajax({
            url: "/api/categoria/",
        }).success(function(data) {
            $('#categoria').html('');
            for(i=0; i<data.length; i++){
                $('#categoria').append("<option value='" + data[i].id + "'>" + data[i].descricao + "</option>");
            }
        })
    });

    carregar_conta = function(){
        $('#conta tbody').html('<tr><td colspan="7" class="text-center"><strong>Carregando...</strong></td></tr>');
        $.ajax({
            url: "/api/conta/ajustar/",
        }).done(function(data) {
            $('#conta tbody').html('<tr></tr>');
            $('#conta tbody tr').attr('data-id', data.id);
            $('#conta tbody tr').append('<td>' + data.orcamento + '</td>');
            $('#conta tbody tr').append('<td>' + data.nome + '</td>');
            $('#conta tbody tr').append('<td>' + data.descricao + '</td>');
            $('#conta tbody tr').append('<td>' + data.previsto + '</td>');
            $('#conta tbody tr').append('<td>' + data.atual + '</td>');
            $('#conta tbody tr').append('<td>' + data.pago + '</td>');
        }).fail(function(){
            $('#conta tbody').html('<tr data-id="-1"><td colspan="7" class="text-center"><strong>Nenhuma conta sem categoria</strong></td></tr>');
        });
    };

    $('#btnEnviar').click(function(e){
        e.preventDefault();
        var conta_id = $('#conta tbody tr').attr('data-id');
        if(conta_id != "-1"){
            var url = "/api/conta/" + conta_id + "/";
            var data = {"categoria": $('#categoria').val()};
            $.ajax({
                method: "PATCH",
                url: url,
                data: data,
            }).done(function(data) {
                carregar_conta();
            });
        }
    });

    $('#refresh_categoria').click();
    carregar_conta();
});
