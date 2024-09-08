document.getElementById('start-test').addEventListener('click', function() {
    document.getElementById('loading').style.display = 'block';

    fetch('/test')
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading').style.display = 'none';

            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('download-speed').innerText = data.download || 'N/A';
                document.getElementById('ping').innerText = data.ping || 'N/A';
            }
        })
        .catch(error => {
            document.getElementById('loading').style.display = 'none';
            console.error('Fetch error:', error);
            alert('An error occurred while fetching the test results.');
        });
});