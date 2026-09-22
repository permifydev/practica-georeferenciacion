const campoVehiculo = document.getElementById(
    "vehiculo"
);

const campoVehiculoId = document.getElementById(
    "vehiculo-id"
);

const formularioViaje = document.getElementById(
    "formulario-viaje"
);

const opcionesVehiculos = document.querySelectorAll(
    "#lista-vehiculos option"
);


function buscarVehiculoSeleccionado() {

    const textoIngresado = campoVehiculo.value
        .trim()
        .replace(/\s+/g, " ")
        .toLowerCase();


    const opcionSeleccionada = Array.from(
        opcionesVehiculos
    ).find(
        function (opcion) {

            const nombreVehiculo = opcion.value
                .trim()
                .replace(/\s+/g, " ")
                .toLowerCase();

            return nombreVehiculo === textoIngresado;
        }
    );


    if (opcionSeleccionada) {

        campoVehiculoId.value =
            opcionSeleccionada.dataset.id;

        return true;
    }


    campoVehiculoId.value = "";

    return false;
}


campoVehiculo.addEventListener(
    "input",
    buscarVehiculoSeleccionado
);


formularioViaje.addEventListener(
    "submit",
    function (evento) {

        const vehiculoValido =
            buscarVehiculoSeleccionado();


        if (!vehiculoValido) {

            evento.preventDefault();

            alert(
                "Selecciona un vehículo válido de la lista."
            );
        }
    }
);


/* =========================================
   MAPA DEL VIAJE
========================================= */

const contenedorMapa = document.getElementById(
    "mapa-viaje"
);


if (contenedorMapa) {

    const origenLat = parseFloat(
        contenedorMapa.dataset.origenLat
    );

    const origenLon = parseFloat(
        contenedorMapa.dataset.origenLon
    );

    const destinoLat = parseFloat(
        contenedorMapa.dataset.destinoLat
    );

    const destinoLon = parseFloat(
        contenedorMapa.dataset.destinoLon
    );


    const origen = [
        origenLat,
        origenLon
    ];

    const destino = [
        destinoLat,
        destinoLon
    ];


    const mapa = L.map(
        "mapa-viaje"
    );


    L.tileLayer(
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }
    ).addTo(mapa);


    L.marker(
        origen
    )
        .addTo(mapa)
        .bindPopup(
            "Origen"
        );


    L.marker(
        destino
    )
        .addTo(mapa)
        .bindPopup(
            "Destino"
        );


    const lineaViaje = L.polyline(
        [
            origen,
            destino
        ]
    ).addTo(mapa);


    mapa.fitBounds(
        lineaViaje.getBounds(),
        {
            padding: [
                40,
                40
            ]
        }
    );
}