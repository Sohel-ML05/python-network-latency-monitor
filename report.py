import csv
import os
from datetime import datetime


def save_report(target_ip, average_latency, packet_loss, network_status):

    os.makedirs("reports", exist_ok=True)

    file_path = "reports/network_report.csv"

    file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0

    with open(file_path, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date",
                "Target IP",
                "Average Latency (ms)",
                "Packet Loss (%)",
                "Network Status"
            ])

        writer.writerow([
            datetime.now(),
            target_ip,
            average_latency,
            packet_loss,
            network_status
        ])

    print("\nCSV report saved successfully!")
    print("File location:", file_path)

    return file_path
