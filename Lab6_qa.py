import subprocess
import json
import time

def client(server_ip):
    return subprocess.run(["iperf3", "-c", server_ip, "--json"], capture_output=True, text=True)

def parser(iperf_result):
    try:
        json_result = json.loads(iperf_result.stdout)
        return list(map(lambda interval: parse_interval(interval), json_result["intervals"]))
    except KeyError:
        return []

def parse_interval(interval):
    interval_sum = interval.get("sum", {})
    return {
        "Interval": f'{interval_sum.get("start", 0):.2f}-{interval_sum.get("end", 0):.2f}',
        "Transfer": float(f'{interval_sum.get("bytes", 0) / (1024 * 1024):.2f}'),
        "Bitrate": float(f'{interval_sum.get("bits_per_second", 0) / 1e6:.1f}'),
        "Retr": float(f'{interval_sum.get("retransmits", 0):.1f}')
    }

if __name__ == "__main__":
    server_ip = '192.168.0.136'
    measurement_duration = 10

    try:
        while True:
            result = client(server_ip)
            result_list = parser(result)

            for value in result_list:
                print(value)
                print("-" * 50)

            print(f"Waiting for {measurement_duration} seconds before next measurement...")
            time.sleep(measurement_duration)

    except KeyboardInterrupt:
        print("Program terminated manually.")
