import subprocess
import re


def check_packet_loss(target_ip):

    result = subprocess.run(
        ["ping", "-c", "10", target_ip],
        capture_output=True,
        text=True
    )

    print("\nPACKET LOSS MONITOR")
    print("---------------------------------")
    print("Target IP:", target_ip)

    match = re.search(r"(\d+)% packet loss", result.stdout)

    if match:
        packet_loss = int(match.group(1))

        print("Packet Loss:", packet_loss, "%")

        if packet_loss == 0:
            print("Network Quality: GOOD")
        else:
            print("Network Quality: PACKET LOSS DETECTED")

        return packet_loss

    else:
        print("Could not calculate packet loss.")
        print(result.stderr)
        return None
