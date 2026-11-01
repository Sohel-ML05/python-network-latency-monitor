from flask import Flask, render_template, request, jsonify
from ping_monitor import check_ping
from latency import check_latency
from packet_loss import check_packet_loss
from traceroute import check_traceroute

from alerts import (
    check_latency as latency_alert,
    check_packet_loss as packet_loss_alert
)

from report import save_report

import ipaddress

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/monitor", methods=["POST"])
def monitor():

    data = request.get_json(silent=True) or {}
    target_ip = data.get("target_ip", "").strip()

    try:
        ipaddress.ip_address(target_ip)
    except ValueError:
        return jsonify({"error": "Please enter a valid IP address."}), 400

    network_status = check_ping(target_ip)

    average_latency = check_latency(target_ip)

    packet_loss = check_packet_loss(target_ip)

    traceroute_result = check_traceroute(target_ip)

    latency_alert(average_latency)

    packet_loss_alert(packet_loss)

    save_report(
        target_ip,
        average_latency,
        packet_loss,
        network_status
    )

    return jsonify({
        "target_ip": target_ip,
        "network_status": network_status,
        "average_latency": average_latency,
        "packet_loss": packet_loss,
        "traceroute": traceroute_result,
        "network_quality": (
            "GOOD" if packet_loss == 0 else "POOR"
            if packet_loss is not None else "UNKNOWN"
        )
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
