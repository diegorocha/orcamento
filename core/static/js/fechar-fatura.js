/**
 * Created by diego on 06/05/17.
 */
$(document).ready(function(){
    $('#btnOk').click(function(e){
        e.preventDefault();
        var fatura = $('#fatura').val();
        var valor_final = $('#valor_final').val();
        var orcamento = $('#orcamento').val();
        var url = "/api/cartao/fatura/" + fatura + "/fechar/";
        var data = {'valor_final': valor_final, 'orcamento': orcamento};

        $.ajax({
             url: url,
             type : "POST",
             data: data,
             success: function() {
                 $('#sucesso').show().delay(5000).fadeOut();
             },
             error: function(xhr, status, error){
                 $('#erro').show().delay(5000).fadeOut();
             }
        });
    });
});