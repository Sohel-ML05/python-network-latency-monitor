def check_latency(latency):

    print("\nLATENCY ALERT")

    if latency is None:
        print("Latency unavailable.")
    elif latency > 100:
        print("WARNING: High latency detected!")
    else:
        print("Latency Status: NORMAL")


def check_packet_loss(packet_loss):

    print("\nPACKET LOSS ALERT")

    if packet_loss is None:
        print("Packet loss unavailable.")
    elif packet_loss > 0:
        print("WARNING: Packet loss detected!")
    else:
        print("Packet Loss Status: NORMAL")
