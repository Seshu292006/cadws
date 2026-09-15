import requests


# =========================
# WORKERS
# =========================

workers = [
    {
        "name": "Kali",
        "url": "http://10.96.208.145:5000"
    },

    {
        "name": "Windows",
        "url": "http://10.96.208.144:5000"
    }
]


# =========================
# GET INFORMATION
# =========================

def get_info(worker):

    try:

        response = requests.get(
            worker["url"] + "/info",
            timeout=3
        )

        return response.json()

    except:

        return None


# =========================
# FIND BEST MACHINE
# =========================

def find_best_worker():

    best_worker = None
    best_score = 999

    for worker in workers:

        info = get_info(worker)

        if info is None:

            print(worker["name"], "OFFLINE")
            continue

        print(
            worker["name"],
            "| OS:", info["os"],
            "| CPU:", info["cpu"], "%",
            "| RAM:", info["memory"], "%"
        )

        # Simple scheduling score
        score = info["cpu"] + info["memory"]

        if score < best_score:

            best_score = score
            best_worker = worker

    return best_worker


# =========================
# RUN TASK
# =========================

def run_task(worker, command):

    print("\nRunning task on", worker["name"])

    response = requests.post(

        worker["url"] + "/run",

        json={
            "command": command
        },

        timeout=60
    )

    result = response.json()

    print("\nOUTPUT:")
    print(result["output"])

    if result["error"]:
        print("\nERROR:")
        print(result["error"])


# =========================
# MAIN
# =========================

print("\nChecking workers...\n")

worker = find_best_worker()


if worker is None:

    print("\nNo worker available.")

else:

    print(
        "\nSelected:",
        worker["name"]
    )

    run_task(
        worker,
        "python3 --version"
    )
