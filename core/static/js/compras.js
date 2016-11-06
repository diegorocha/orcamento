$('.comprado').show();

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

$('input.comprado').click(function(){
    var id = $(this).attr('data-id');
    var checked = $(this).is(':checked');
    var tr = $('tr[data-id=' + id + ']'); 
    if(checked){
        tr.removeClass('item-nao-comprado');
    }else{
        tr.addClass('item-nao-comprado');
    }
    var url = "/api/compras/itens-compra/" + id + "/";
    var dados = {'comprado': checked};
    $.ajax({
        url: url,
        type : "PATCH",
        data: dados,
        success: function(result) {
            console.log(result);
            tr.addClass('success');
            setTimeout(function(){
                tr.removeClass('success');
            }, 2000);
        }
    });
});

$('input.comprar').click(function(){
    var id = $(this).attr('data-id');
    var checked = $(this).is(':checked');
    if($(this).is(':checked')){
        $('tr[data-id=' + id + ']').removeClass('nao-comprar');
        $('tr[data-id=' + id + ']').attr('data-comprar', 'True');

    }else{
        $('tr[data-id=' + id + ']').addClass('nao-comprar');
        $('tr[data-id=' + id + ']').attr('data-comprar', 'False');
    }
    var url = "/api/compras/itens-compra/" + id + "/";
    var dados = {'comprar': checked};
    $.ajax({
        url: url,
        type : "PATCH",
        data: dados,
        success: function(result) {
            console.log(result);
            tr.addClass('success');
            setTimeout(function(){
                tr.removeClass('success');
            }, 2000);
        }
    });
});

$('#cbFiltroComprar').click(function(){
    if($(this).is(':checked')){
        $('tr[data-comprar="False"]').hide();
    }else{
        $('tr[data-comprar="False"]').show();
    }
});