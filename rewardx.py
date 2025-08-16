import requests
import time
import json
import urllib.parse
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama
init(autoreset=True)

# === CONFIG ===
LOOPS = 30
DELAY_BETWEEN_ACCOUNTS = 1
DELAY_BETWEEN_LOOPS = 3

HEADERS = {
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

# === Banner ===
def banner():
    print(Fore.GREEN + Style.BRIGHT + pyfiglet.figlet_format("Code2crypto"))
    print(Fore.GREEN + "          🚀 Developed by Anaik_Dev 🚀\n")

# === Encode Query ===
def double_encode_if_needed(init_data: str) -> str:
    """If init_data is not double-encoded, double-encode it."""
    if "%25" in init_data:
        return init_data  # already double encoded
    return urllib.parse.quote(init_data, safe='')

# === API Calls ===
def get_task_id(init_data):
    url = f"https://botsmother.com/api/command/MTE3NQ==/OTUzNQ==?initData={init_data}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(Fore.GREEN + "First response raw:", r.text)
        data = json.loads(r.text)
        return data.get("task_id")
    except json.JSONDecodeError:
        print(Fore.RED + "Error: Response was not valid JSON")
        return None
    except Exception as e:
        print(Fore.RED + "Request failed:", str(e))
        return None

def send_reward(init_data, task_id):
    url = f"https://botsmother.com/api/command/MTE3NQ==/OTUzNg==?initData={init_data}&task_id={task_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(Fore.GREEN + "Second response raw:", r.text)
    except Exception as e:
        print(Fore.RED + "Reward request failed:", str(e))

# === Main ===
if __name__ == "__main__":
    banner()
    
    query_id = input(Fore.GREEN + Style.BRIGHT + "Enter your Query ID: ").strip()
    if not query_id:
        print(Fore.RED + "No Query ID provided. Exiting...")
        exit()

    init_data = double_encode_if_needed(query_id)

    for loop in range(1, LOOPS + 1):
        print(Fore.GREEN + f"\n=== Loop {loop}/{LOOPS} ===")
        task_id = get_task_id(init_data)
        time.sleep(15)
        if task_id:
            send_reward(init_data, task_id)
        else:
            print(Fore.RED + "Skipping reward, no task_id found.")
        time.sleep(DELAY_BETWEEN_ACCOUNTS)

        if loop != LOOPS:
            time.sleep(DELAY_BETWEEN_LOOPS)