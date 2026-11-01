import subprocess


def check_traceroute(target_ip):

    result = subprocess.run(
        ["traceroute", "-m", "10", target_ip],
        capture_output=True,
        text=True
    )

    print("\nTRACEROUTE MONITOR")
    print("---------------------------------")
    print("Target IP:", target_ip)

    print("\nNETWORK ROUTE:")
    print(result.stdout)

    if result.returncode == 0:
        print("Traceroute completed.")
        return result.stdout
    else:
        print("Traceroute could not complete.")
        print(result.stderr)
        return None
