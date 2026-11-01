from ping_monitor import check_ping
from latency import check_latency
from packet_loss import check_packet_loss
from traceroute import check_traceroute

from alerts import (
    check_latency as latency_alert,
    check_packet_loss as packet_loss_alert
)

from report import save_report


def main():

    print("\n====================================")
    print(" NETWORK MONITORING TOOL")
    print("====================================")

    target_ip = input("Enter target IP address: ")

    # 1. Check connectivity
    network_status = check_ping(target_ip)

    # 2. Measure latency
    average_latency = check_latency(target_ip)

    # 3. Calculate packet loss
    packet_loss = check_packet_loss(target_ip)

    # 4. Analyze network route
    check_traceroute(target_ip)

    # 5. Generate alerts
    latency_alert(average_latency)
    packet_loss_alert(packet_loss)

    # 6. Save CSV report
    save_report(
        target_ip,
        average_latency,
        packet_loss,
        network_status
    )

    print("\n====================================")
    print(" MONITORING COMPLETED")
    print("====================================")


if __name__ == "__main__":
    main()
