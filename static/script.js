// static/script.js

$(document).ready(function() {

      // Evento para limpiar resultados
      $('#limpiar-ruta').on('click', function(event) {
        event.preventDefault();
        $('#ruta').empty(); // Limpiar resultados de la ruta
        $('#distancia').empty(); // Limpiar distancia
        $('#dijkstra-ruta').empty(); // Limpiar resultados de Dijkstra
        $('#genetico-ruta').empty(); // Limpiar resultados de Algoritmo Genético
        $('#mapa').hide(); // Ocultar el mapa interactivo
    });
    
    $('#ruta-form').on('submit', function(event) {
        event.preventDefault();

        const partida = $('#partida').val();
        const destino = $('#destino').val();

        $.ajax({
            url: '/ruta',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                partida: partida,
                destino: destino
            }),
            success: function(response) {
                $('#ruta').html('<strong>Ruta:</strong> ' + response.ruta);
                $('#distancia').html('<strong>Distancia:</strong> ' + response.distancia);
                mostrarRuta(response.algoritmo_optimo.resultados, '#dijkstra-ruta');
                mostrarRuta(response.algoritmo_optimo.resultados, '#genetico-ruta');
                $('#mapa').attr('src', '/static/ruta_interactiva.html').show();
            },
            error: function(error) {
                $('#resultados').html('<strong>Error:</strong> No se encontró una ruta válida para los destinos seleccionados.');
            }
        });

        function mostrarRuta(ruta, destino) {
            $(destino).empty();
            ruta.forEach(function(nodo) {
                $(destino).append('<li>' + nodo + '</li>');
            });
        }
    });
});
