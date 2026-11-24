import time
import sys
from datetime import datetime
import urllib.request

def ping_loop(url: str, interval_minutes: int = 14):
    interval_seconds = interval_minutes * 60
    print("=" * 60)
    print("Starting Keep-Alive Ping Service")
    print(f"Target URL: {url}")
    print(f"Interval: Every {interval_minutes} minutes ({interval_seconds} seconds)")
    print("=" * 60)

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Render-KeepAlive-Bot/1.0"}
            )
            start_time = time.time()
            with urllib.request.urlopen(req, timeout=30) as response:
                status = response.status
                latency_ms = (time.time() - start_time) * 1000
                print(f"[{timestamp}] PING SUCCESS -> Status: {status} | Latency: {latency_ms:.1f}ms")
        except Exception as e:
            print(f"[{timestamp}] PING ERROR -> {e}")

        time.sleep(interval_seconds)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://gcv-predictor.onrender.com"
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    ping_loop(target, interval)
