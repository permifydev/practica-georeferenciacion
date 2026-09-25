const formularioCargadores = document.getElementById(
    "formulario-cargadores"
);

const campoDireccion = document.getElementById(
    "direccion"
);

const campoLatitud = document.getElementById(
    "latitud"
);

const campoLongitud = document.getElementById(
    "longitud"
);

const botonUbicacion = document.getElementById(
    "boton-ubicacion"
);


botonUbicacion.addEventListener(
    "click",
    function () {

        botonUbicacion.disabled = true;

        botonUbicacion.textContent =
            "Obteniendo ubicación...";


        obtenerUbicacionActual(

            function (
                latitud,
                longitud
            ) {

                campoLatitud.value =
                    latitud;

                campoLongitud.value =
                    longitud;

                campoDireccion.value =
                    "";

                formularioCargadores.submit();
            },


            function () {

                alert(
                    "No fue posible obtener tu ubicación."
                );

                botonUbicacion.disabled = false;

                botonUbicacion.textContent =
                    "Usar mi ubicación actual";
            }

        );

    }
);


formularioCargadores.addEventListener(
    "submit",
    function (evento) {

        const direccion =
            campoDireccion.value.trim();

        const tieneCoordenadas =
            campoLatitud.value &&
            campoLongitud.value;


        if (
            !direccion &&
            !tieneCoordenadas
        ) {

            evento.preventDefault();

            alert(
                "Ingresa una dirección o usa tu ubicación actual."
            );

            return;
        }


        if (direccion) {

            campoLatitud.value = "";

            campoLongitud.value = "";
        }

    }
);


/* =========================================
   MAPA DE CARGADORES
========================================= */

const contenedorMapa = document.getElementById(
    "mapa-cargadores"
);


if (contenedorMapa) {

    const usuarioLat = parseFloat(
        contenedorMapa.dataset.usuarioLat
    );

    const usuarioLon = parseFloat(
        contenedorMapa.dataset.usuarioLon
    );

    const botonGoogleMaps = document.getElementById(
        "boton-google-maps"
    );


    const mapa = L.map(
        "mapa-cargadores"
    );


    L.tileLayer(
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,
            attribution:
                '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }
    ).addTo(mapa);


    const ubicacionUsuario = [
        usuarioLat,
        usuarioLon
    ];


    const puntosMapa = [
        ubicacionUsuario
    ];


    /* =========================================
       UBICACIÓN DEL USUARIO
    ========================================= */

    L.circleMarker(
        ubicacionUsuario,
        {
            radius: 10,
            weight: 3,
            fillOpacity: 1
        }
    )
        .addTo(mapa)
        .bindPopup(
            "<strong>Tu ubicación</strong>"
        );


    /* =========================================
       CARGADORES
    ========================================= */

    const datosCargadores = document.querySelectorAll(
        ".dato-cargador"
    );


    const marcadoresCargadores = [];


    datosCargadores.forEach(
        function (
            cargador,
            indice
        ) {

            const latitud = parseFloat(
                cargador.dataset.lat
            );

            const longitud = parseFloat(
                cargador.dataset.lon
            );

            const nombre =
                cargador.dataset.nombre;

            const distancia =
                cargador.dataset.distancia;


            if (
                Number.isNaN(latitud) ||
                Number.isNaN(longitud)
            ) {

                return;
            }


            const posicion = [
                latitud,
                longitud
            ];


            const marcador = L.marker(
                posicion
            )
                .addTo(mapa)
                .bindPopup(
                    `
                    <strong>
                        ${indice + 1}. ${nombre}
                    </strong>
                    <br>
                    Distancia aproximada:
                    ${distancia} km
                    `
                );


            marcadoresCargadores.push(
                {
                    nombre:
                        nombre,
                    latitud:
                        latitud,
                    longitud:
                        longitud,
                    marcador:
                        marcador
                }
            );


            puntosMapa.push(
                posicion
            );

        }
    );


    /* =========================================
       AJUSTAR MAPA
    ========================================= */

    mapa.fitBounds(
        puntosMapa,
        {
            padding: [
                40,
                40
            ]
        }
    );


    /* =========================================
       SELECCIONAR CARGADOR
    ========================================= */

    const botonesCargadores =
        document.querySelectorAll(
            ".boton-cargador"
        );


    let lineaSeleccionada = null;


    botonesCargadores.forEach(
        function (
            boton
        ) {

            boton.addEventListener(
                "click",
                function () {

                    const latitud = parseFloat(
                        boton.dataset.lat
                    );

                    const longitud = parseFloat(
                        boton.dataset.lon
                    );

                    
                    const nombre =
                        boton.dataset.nombre;


                    if (
                        Number.isNaN(latitud) ||
                        Number.isNaN(longitud)
                    ) {

                        return;
                    }

                    const urlGoogleMaps =
                        "https://www.google.com/maps/dir/?api=1"
                        + `&origin=${usuarioLat},${usuarioLon}`
                        + `&destination=${latitud},${longitud}`
                        + "&travelmode=driving";


                    botonGoogleMaps.href =
                        urlGoogleMaps;

                    botonGoogleMaps.hidden =
                        false;


                    const posicionCargador = [
                        latitud,
                        longitud
                    ];


                    /* Eliminar línea anterior */

                    if (
                        lineaSeleccionada
                    ) {

                        mapa.removeLayer(
                            lineaSeleccionada
                        );
                    }


                    /* Dibujar nueva línea */

                    lineaSeleccionada = L.polyline(
                        [
                            ubicacionUsuario,
                            posicionCargador
                        ],
                        {
                            weight: 4
                        }
                    ).addTo(mapa);


                    /* Buscar marcador seleccionado */

                    const cargadorEncontrado =
                        marcadoresCargadores.find(
                            function (
                                cargador
                            ) {

                                return (
                                    cargador.latitud ===
                                        latitud
                                    &&
                                    cargador.longitud ===
                                        longitud
                                );
                            }
                        );


                    if (
                        cargadorEncontrado
                    ) {

                        cargadorEncontrado
                            .marcador
                            .openPopup();
                    }


                    /* Centrar usuario y cargador */

                    mapa.fitBounds(
                        [
                            ubicacionUsuario,
                            posicionCargador
                        ],
                        {
                            padding: [
                                70,
                                70
                            ]
                        }
                    );

                }
            );

        }
    );

}