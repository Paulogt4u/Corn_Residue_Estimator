document.getElementById('getStarted').addEventListener('click', function() {
    var map = L.map('map').setView([45.4215, -75.6972], 13); // Set to your desired initial coordinates

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    map.on('click', function(e) {
        let lat = e.latlng.lat;
        let lng = e.latlng.lng;

        fetch('/calculate-residue', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ latitude: lat, longitude: lng })
        })
        .then(response => response.json())
        .then(data => {
            alert(`Residue: ${data.residue} Mg ha-1, Stability Zone: ${data.stability_zone}`);
        })
        .catch(error => console.error('Error:', error));
    });
});
