import requests
import time
from requests.exceptions import ConnectionError, Timeout, RequestException

def download_speed_test(url, num_connections=4):
    try:
        def download_part(url, start, end):
            headers = {"Range": f"bytes={start}-{end}"}
            response = requests.get(url, headers=headers, stream=True)
            return len(response.content)

        file_size = int(requests.head(url, timeout=10).headers.get('Content-Length', 0))
        if file_size == 0:
            print("Failed to retrieve file size.")
            return

        chunk_size = file_size // num_connections

        start_time = time.time()

        data_downloaded = 0
        for i in range(num_connections):
            start = i * chunk_size
            end = start + chunk_size if i < num_connections - 1 else file_size
            data_downloaded += download_part(url, start, end)

        end_time = time.time()

        time_taken = end_time - start_time
        speed = data_downloaded / time_taken  # Bytes per second
        speed_mbps = (speed * 8) / (1024 * 1024)  # Convert to Megabits per second (Mbps)

        print(f"Download speed: {speed_mbps:.2f} Mbps")

    except ConnectionError:
        print("Connection error occurred. Please check your internet connection or try a different server.")
    except Timeout:
        print("The request timed out. Please try again later.")
    except RequestException as e:
        print(f"An error occurred: {e}")

download_speed_test("http://speedtest.tele2.net/10MB.zip")