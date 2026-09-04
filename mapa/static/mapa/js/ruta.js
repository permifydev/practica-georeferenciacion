const botones = document.querySelectorAll(".transporte");
const tiempoTexto = document.getElementById("tiempo-texto");

botones.forEach((boton) => {
    boton.addEventListener("click", () => {

        botones.forEach((b) => {
            b.classList.remove("activo");
        });

        boton.classList.add("activo");

        const tiempo = boton.dataset.tiempo;
        const nombre = boton.dataset.nombre;
        const icono = boton.dataset.icono;

        tiempoTexto.innerHTML = `
            <strong>${icono} ${nombre}</strong><br>
            ${tiempo}
        `;
    });
});

const mapaElemento = document.getElementById("mapa-ruta");

if (mapaElemento) {

    const origenLat = parseFloat(mapaElemento.dataset.origenLat);
    const origenLon = parseFloat(mapaElemento.dataset.origenLon);

    const destinoLat = parseFloat(mapaElemento.dataset.destinoLat);
    const destinoLon = parseFloat(mapaElemento.dataset.destinoLon);

    const mapa = L.map("mapa-ruta");

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap"
    }).addTo(mapa);

    const marcadorOrigen = L.marker([
        origenLat,
        origenLon
    ]).addTo(mapa);

    marcadorOrigen.bindPopup("Origen");

    const marcadorDestino = L.marker([
        destinoLat,
        destinoLon
    ]).addTo(mapa);

    marcadorDestino.bindPopup("Destino");

    const puntos = [
        [origenLat, origenLon],
        [destinoLat, destinoLon]
    ];

        L.polyline(puntos, { /*dibuja la linea entre los dos puntos de la ubicasiones */
        weight: 5,
        opacity: 0.8
    }).addTo(mapa);

    mapa.fitBounds(puntos, {
        padding: [40, 40]
    });
}