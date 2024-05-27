
$(document).ready(function(){
    $('.add-to-cart').on('click', function(){
        const idcan= $(this).data('id');
        const titulocan =$(this).data('titulo');
        const preciocan =$(this).data('precio');

        $.post('/agregar_carrito', {
            id:idcan,
            titulo:titulocan,
            precio:preciocan


        }, function(){
            window.location.href='/Lista_canciones_u';
        });

    });
    $('.eliminar_uno_').on('click', function(){
        const id_eliminar= $(this).data('id');

        $.post('/eliminar_uno', {
            id :id_eliminar
        }, function(){
            window.location.href='/carrito';
        });
    });

});






