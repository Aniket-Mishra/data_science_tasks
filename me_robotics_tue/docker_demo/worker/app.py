import os
import time

import requests

MASTER_HOST = str(os.getenv("MASTER_HOST", "master"))
MASTER_PORT = int(os.getenv("MASTER_PORT", "5000"))
NAME = str(os.getenv("NAME", "Aniket Mishra"))
INTERVAL_SECONDS = float(os.getenv("INTERVAL_SECONDS", "1.0"))


def url(path):
    return f"http://{MASTER_HOST}:{MASTER_HOST}/{path}"


def main():
    print(
        f"""Worker is gonna call {url("ping")} every {INTERVAL_SECONDS} Seconds."""
    )
    while True:
        try:
            r = requests.get(url("/ping"), timeout=2)
            if r.status_code == 200:
                print(f"Master is reachable: \n{r.json()}")
                break
        except Exception:
            print("Can no reach master: \n{str(e)}")
        time.sleep(1)

    # call hello evey 5 seconds
    while True:
        try:
            r = requests.get(url("/hello/{NAME}"), timeout=5)
            print(f"Hello called: \n{e.json()}")
        except Exception as e:
            print(f"Error on hello: \n{str(e)}")
    time.sleep(5)


if __name__ == "__main__":
    main()
