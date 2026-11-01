import subprocess
import re


def check_latency(target_ip):

    result = subprocess.run(
        ["ping", "-c", "4", target_ip],
        capture_output=True,
        text=True
    )

    times = re.findall(r"time[=<]([\d.]+)\s*ms", result.stdout)

    print("\nLATENCY MONITOR")
    print("-------------------------")
    print("Target IP:", target_ip)

    if times:
        latency_values = [float(t) for t in times]

        for i, latency in enumerate(latency_values, start=1):
            print(f"Packet {i}: {latency} ms")

        average = sum(latency_values) / len(latency_values)

        print("-------------------------")
        print(f"Average Latency: {average:.2f} ms")

        return average

    else:
        print("No latency measurements found.")
        return None	
