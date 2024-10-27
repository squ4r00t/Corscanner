import requests
import argparse
import os

# Define color variables
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# CORS headers
ACAO_STR = "access-control-allow-origin"
ACAC_STR = "access-control-allow-credentials"

def test_url(url, valid_origin):
    print(f"{YELLOW}[i] Url: {url}{RESET}")
    payloads = ["https://evil.com", "null"]

    if valid_origin != "":
        payloads.append(f"https://{valid_origin}")
        payloads.append(f"https://{valid_origin}.evil.com")
        payloads.append(f"https://evil{valid_origin}")
        payloads.append(f"https://evil.com/{valid_origin}")

    for payload in payloads:
        print(f"{BLUE}[i] Testing {payload}{RESET}")
        headers = {
            'Origin': payload,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 GLS/100.10.9939.100'
        }
        response = requests.get(url, headers=headers)

        # Checking CORS headers in response
        if ACAO_STR in response.headers and ACAC_STR in response.headers:
            if response.headers.get(ACAO_STR) == payload and response.headers.get(ACAC_STR) == "true":
                print(f"{GREEN}[+] [{response.status_code}] - {url} is vulnerable to the payload -> Origin: {payload}{RESET}")
                print(f"{GREEN}[+] Access-Control-Allow-Origin: {response.headers.get(ACAO_STR)}{RESET}")
                print(f"{GREEN}[+] Access-Control-Allow-Credentials: {response.headers.get(ACAC_STR)}{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detects CORS misconfigurations in a URL or a list of URLs")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", type=str, help="A single URL to process.")
    group.add_argument("--file", type=str, help="A path to a file containing URLs.")

    parser.add_argument("--valid-origin", type=str, help="A valid origin that is accepted by the server")

    args = parser.parse_args()

    if args.url:
        print(f"{MAGENTA}[!] Better be a valid url, didn't check for it...{RESET}")
        if args.valid_origin:
            test_url(args.url, args.valid_origin)
        else:
            test_url(args.url, "")
    elif args.file:
        if not os.path.isfile(args.file):
            print(f"{RED}[-] The file '{args.file}' does not exist.{RESET}")
            exit(1)
        else:
            print(f"501 - Not implemented, coming soon...")
