let latencyChart = null;
let packetChart = null;

let latencyHistory = [];
let packetHistory = [];
let timeLabels = [];

async function startMonitoring() {
    const targetIP = document.getElementById("targetIP").value.trim();
    const monitorBtn = document.getElementById("monitorBtn");
    const monitorMessage = document.getElementById("monitorMessage");

    if (!targetIP) {
        monitorMessage.textContent = "Please enter an IP address.";
        return;
    }

    monitorBtn.disabled = true;
    monitorBtn.textContent = "Monitoring...";
    monitorMessage.textContent = "Collecting network data. Please wait...";

    try {
        const response = await fetch("/api/monitor", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                target_ip: targetIP
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Monitoring failed.");
        }

        updateDashboard(data);
        monitorMessage.textContent = "Monitoring completed successfully.";

    } catch (error) {
        monitorMessage.textContent = "Error: " + error.message;

    } finally {
        monitorBtn.disabled = false;
        monitorBtn.textContent = "Start Monitoring";
    }
}

function updateDashboard(data) {
    document.getElementById("networkStatus").textContent =
        data.network_status || "--";

    document.getElementById("averageLatency").textContent =
        data.average_latency === null
            ? "--"
            : Number(data.average_latency).toFixed(2) + " ms";

    document.getElementById("packetLoss").textContent =
        data.packet_loss === null
            ? "--"
            : data.packet_loss + "%";

    document.getElementById("networkQuality").textContent =
        data.network_quality || "UNKNOWN";

    document.getElementById("tracerouteOutput").textContent =
        data.traceroute || "Traceroute unavailable.";

    updateAlerts(data);
    updateHistory(data);
    updateCharts(data);
}

function updateAlerts(data) {
    const alertOutput = document.getElementById("alertOutput");
    const messages = [];

    if (data.average_latency === null) {
        messages.push("Latency measurement unavailable.");
    } else if (data.average_latency > 100) {
        messages.push("WARNING: High latency detected!");
    } else {
        messages.push("Latency status: NORMAL");
    }

    if (data.packet_loss === null) {
        messages.push("Packet loss measurement unavailable.");
    } else if (data.packet_loss > 0) {
        messages.push("WARNING: Packet loss detected!");
    } else {
        messages.push("Packet loss status: NORMAL");
    }

    alertOutput.textContent = messages.join("\n");
}

function updateHistory(data) {
    const historyOutput = document.getElementById("historyOutput");
    const row = document.createElement("p");

    const latency = data.average_latency === null
        ? "N/A"
        : Number(data.average_latency).toFixed(2) + " ms";

    row.textContent =
        new Date().toLocaleTimeString() +
        " | " + data.target_ip +
        " | " + data.network_status +
        " | Latency: " + latency +
        " | Packet Loss: " +
        (data.packet_loss === null ? "N/A" : data.packet_loss + "%");

    historyOutput.prepend(row);
}

function updateCharts(data) {
    if (typeof Chart === "undefined") {
        return;
    }

    const currentTime = new Date().toLocaleTimeString();

    timeLabels.push(currentTime);
    latencyHistory.push(data.average_latency);
    packetHistory.push(data.packet_loss);

    if (timeLabels.length > 10) {
        timeLabels.shift();
        latencyHistory.shift();
        packetHistory.shift();
    }

    if (latencyChart) {
        latencyChart.destroy();
    }

    if (packetChart) {
        packetChart.destroy();
    }

    const latencyCanvas = document.getElementById("latencyChart");
    const packetCanvas = document.getElementById("packetChart");

    if (latencyCanvas) {
        latencyChart = new Chart(latencyCanvas, {
            type: "line",
            data: {
                labels: timeLabels,
                datasets: [{
                    label: "Latency (ms)",
                    data: latencyHistory,
                    borderColor: "#38bdf8",
                    backgroundColor: "rgba(56, 189, 248, 0.15)",
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    if (packetCanvas) {
        packetChart = new Chart(packetCanvas, {
            type: "line",
            data: {
                labels: timeLabels,
                datasets: [{
                    label: "Packet Loss (%)",
                    data: packetHistory,
                    borderColor: "#a78bfa",
                    backgroundColor: "rgba(167, 139, 250, 0.15)",
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: 0,
                        max: 100
                    }
                }
            }
        });
    }
}
