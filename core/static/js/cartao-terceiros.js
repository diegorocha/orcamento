$(document).ready(function(){
    function getTotal(selector){
        return $(selector)
            .map(function(){
                return parseFloat(
                    $(this).text().replace(",", ".") || 0
                );
            })
            .toArray()
            .reduce(function (previousValue, currentValue) {
                return previousValue + currentValue;
            });
    }

    function atualizaTotais(){
        var totais = ["real", "dolar"];
        totais.forEach(function (value) {
           var total = getTotal(".compra-renata-valor-" + value);
           $(".compra-renata-total-" + value).text(total.toFixed(2).replace(".", ","));
        });
    }

    $('.mudar-categoria').click(function(){
        var parent = $(this).parent().parent();
        var id = parent.data('id');
        var categoria = parent.data('categoria');
        var nova_categoria = parent.find('select').val();

        if(nova_categoria !== categoria){
            var payload = {
                'categoria': nova_categoria
            };
            $.ajax({
                type: "PATCH",
                url: "/api/cartao/compra/" + id + "/",
                data: payload,
                success: function() {
                    parent.remove();
                    atualizaTotais();
                },
                error: function(xhr, status, error){
                    console.log(error);
                }
            });
        }
    });
});
