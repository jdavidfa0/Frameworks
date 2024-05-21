
$(document).ready(function(){
    $('.add-to-cart').on('click', function(){
        const idcan= $(this).data('id');
        const titulocan =$(this).data('titulo');
        const preciocan =$(this).data('precio');

        $.post('/agregar_carrito', {
            id:idcan,
            titulo:titulocan,
            precio:preciocan


        }, function(data){
            alert(data.message || 'Error al agregar la canción');
        });

    });
});