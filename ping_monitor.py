import subprocess


def check_ping(target_ip):

    result = subprocess.run(
        ["ping", "-c", "4", target_ip],
        capture_output=True,
        text=True
    )

    print("\nNETWORK CONNECTIVITY MONITOR")
    print("----------------------------------")
    print("Target IP:", target_ip)
    print("\nPING OUTPUT:")
    print(result.stdout)

    if result.returncode == 0:
        print("Network Status: ONLINE")
        return "ONLINE"
    else:
        print("Network Status: OFFLINE")
        return "OFFLINE"
