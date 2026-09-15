function obtenerUbicacionActual(exito, error) {

    if (!navigator.geolocation) {

        alert(
            "Tu navegador no permite obtener la ubicación."
        );

        return;
    }

    navigator.geolocation.getCurrentPosition(
        function(posicion) {

            const latitud =
                posicion.coords.latitude;

            const longitud =
                posicion.coords.longitude;

            exito(
                latitud,
                longitud
            );
        },

        function(errorUbicacion) {

            if (error) {
                error(errorUbicacion);
                return;
            }

            alert(
                "No fue posible obtener tu ubicación."
            );
        },

        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}
