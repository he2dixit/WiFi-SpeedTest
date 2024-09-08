from flask import Flask, jsonify, render_template
import requests
import time
from requests.exceptions import ConnectionError, Timeout, RequestException
from ping3 import ping

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    speed_result = download_speed_test("http://speedtest.tele2.net/10MB.zip")
    ping_result = ping_test("google.com")
    return jsonify({
        "download": speed_result,
        "ping": ping_result
    })

def download_speed_test(url, num_connections=4):
    try:
        def download_part(url, start, end):
            headers = {"Range": f"bytes={start}-{end}"}
            response = requests.get(url, headers=headers, stream=True)
            return len(response.content)

        file_size = int(requests.head(url, timeout=10).headers.get('Content-Length', 0))
        if file_size == 0:
            return {"error": "Failed to retrieve file size."}

        chunk_size = file_size // num_connections

        start_time = time.time()

        data_downloaded = 0
        for i in range(num_connections):
            start = i * chunk_size
            end = start + chunk_size if i < num_connections - 1 else file_size
            data_downloaded += download_part(url, start, end)

        end_time = time.time()

        time_taken = end_time - start_time
        speed = data_downloaded / time_taken  
        speed_mbps = (speed * 8) / (1024 * 1024) 

        return f"{speed_mbps:.2f} Mbps"

    except ConnectionError:
        return "Connection error occurred. Please check your internet connection or try a different server."
    except Timeout:
        return "The request timed out. Please try again later."
    except RequestException as e:
        return str(e)

def ping_test(server):
    try:
        ping_time = ping(server)
        if ping_time is None:
            return "Ping failed."
        return f"{ping_time * 1000:.2f} ms"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)