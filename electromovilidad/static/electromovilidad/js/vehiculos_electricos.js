const campoVehiculo = document.getElementById(
    "vehiculo"
);

const botonConsultar = document.getElementById(
    "boton-consultar"
);

const fichaVehiculo = document.getElementById(
    "ficha-vehiculo"
);

const opcionesVehiculos = document.querySelectorAll(
    "#lista-vehiculos option"
);


botonConsultar.addEventListener(
    "click",
    function () {

        const textoSeleccionado = normalizarTexto(
            campoVehiculo.value
        );


        const opcionSeleccionada = Array.from(
            opcionesVehiculos
        ).find(
            function (opcion) {

                return normalizarTexto(
                    opcion.value
                ) === textoSeleccionado;
            }
        );


        if (!opcionSeleccionada) {

            fichaVehiculo.hidden = true;

            alert(
                "Selecciona un vehículo válido."
            );

            return;
        }


        mostrarFicha(
            opcionSeleccionada
        );
    }
);


function normalizarTexto(texto) {

    return texto
        .trim()
        .replace(/\s+/g, " ")
        .toLowerCase();
}


function mostrarFicha(vehiculo) {

    document.getElementById(
        "ficha-marca"
    ).textContent = vehiculo.dataset.marca;


    document.getElementById(
        "ficha-modelo"
    ).textContent = vehiculo.dataset.modelo;


    document.getElementById(
        "ficha-version"
    ).textContent = vehiculo.dataset.version;


    document.getElementById(
        "ficha-bateria"
    ).textContent = vehiculo.dataset.bateria;


    document.getElementById(
        "ficha-autonomia"
    ).textContent = vehiculo.dataset.autonomia;


    document.getElementById(
        "ficha-carga"
    ).textContent = vehiculo.dataset.carga;


    fichaVehiculo.hidden = false;
}