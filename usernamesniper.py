import requests
import time
from pystyle import Colors, Colorate
import ctypes
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
import json
import os

def load_proxy_info():
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(script_dir, 'config.json')
        
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}config.json file not found{Style.RESET_ALL}")
        exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error decoding config.json{Style.RESET_ALL}")
        exit(1)

proxy_info = load_proxy_info()

proxies = {
    'http': f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['hostname']}:{proxy_info['port']}",
    'https': f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['hostname']}:{proxy_info['port']}"
}

def ascii():
    print(Colorate.Color(Colors.dark_green, """
 ██▀███   ▒█████    ▄▄▄▄    ██▓    ▒█████  ▒██   ██▒      ██████  ███▄    █   ██ ██▓███  ▓█████ ██▀███  
▓██ ▒ ██▒▒██▒  ██▒ ▓█████▄ ▓██▒   ▒██▒  ██▒▒▒ █ █ ▒░    ▒██    ▒  ██ ▀█   █ ▒▓██▓██░  ██ ▓█   ▀▓██ ▒ ██▒
▓██ ░▄█ ▒▒██░  ██▒ ▒██▒ ▄██▒██░   ▒██░  ██▒░░  █   ░    ░ ▓██▄   ▓██  ▀█ ██▒░▒██▓██░ ██▓▒▒███  ▓██ ░▄█ ▒
▒██▀▀█▄  ▒██   ██░ ▒██░█▀  ▒██░   ▒██   ██░ ░ █ █ ▒       ▒   ██▒▓██▒  ▐▌██▒ ░██▒██▄█▓▒ ▒▒▓█  ▄▒██▀▀█▄  
░██▓ ▒██▒░ ████▓▒░▒░▓█  ▀█▓░██████░ ████▓▒░▒██▒ ▒██▒    ▒██████▒▒▒██░   ▓██░ ░██▒██▒ ░  ░░▒████░██▓ ▒██▒
░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░░▒▓███▀▒░ ▒░▓  ░ ▒░▒░▒░ ▒▒ ░ ░▓ ░    ▒ ▒▓▒ ▒ ░░ ▒░   ▒ ▒  ░▓ ▒▓▒░ ░  ░░░ ▒░ ░ ▒▓ ░▒▓░
  ░▒ ░ ▒░  ░ ▒ ▒░ ░▒░▒   ░ ░ ░ ▒    ░ ▒ ▒░ ░░   ░▒ ░    ░ ░▒  ░  ░ ░░   ░ ▒░  ▒ ░▒ ░      ░ ░    ░▒ ░ ▒░
   ░   ░ ░ ░ ░ ▒    ░    ░   ░ ░  ░ ░ ░ ▒   ░    ░      ░  ░  ░     ░   ░ ░   ▒ ░░          ░     ░   ░ 
   ░         ░ ░  ░ ░          ░      ░ ░   ░    ░            ░           ░   ░             ░     ░     
                         
"""))

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def testproxy():
    url = 'https://ifconfig.me/'
    response = requests.get(url, proxies=proxies)
    ctypes.windll.kernel32.SetConsoleTitleW(response.text)
    time.sleep(5)

def validate_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    headers = {
        "User-Agent": "insomnia/2023.5.8"
    }
    
    response = requests.get(url, headers=headers, proxies=proxies)
    
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            print(f"{Fore.GREEN}[+] {username} {Style.RESET_ALL}")
            with open('valid.txt', 'a') as file:
                file.write(username + '\n')
            return True, username
        elif data['code'] == 1:
            print(f"{Fore.RED}[-] {username} {Style.RESET_ALL}")
        elif data['code'] == 2:
            print(f"{Fore.RED}[-] {username} {Style.RESET_ALL}")
        elif data['code'] == 10:
            print(f"{Fore.YELLOW}[-] {username} {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Unable to access Roblox API{Style.RESET_ALL}")
    
    return False, username

def snipe():
    with open('usernames.txt', 'r') as file:
        usernames = [line.strip() for line in file.readlines()]

    total_usernames = len(usernames)
    available_usernames = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(validate_username, username): username for username in usernames}

        checked_count = 0
        for future in as_completed(futures):
            checked_count += 1
            set_console_title(f"{checked_count}/{total_usernames} - Checking usernames")

    set_console_title("Username Sniper - Finished Checking")

testproxy()
ascii()
snipe()

input("All usernames have been checked. Press Enter to exit...")