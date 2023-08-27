import requests
from colorama import Fore
import json

def check_cors_vulnerability(url, method="GET", headers_list=None,origins_list=None, ignore_404=False):
    base_domain = url.split("//")[-1].split("/")[0]

    test_origins = [
        "https://malicious.com",     
        f"http://sub.{base_domain}",  
    ]

    if origins_list:
        for origin in origins_list:
            test_origins.append(origin)

    for test_origin in test_origins:
        headers = {
            "Origin": test_origin
        }

        if headers_list:
            for header in headers_list:
                name, value = header.split(": ", 1)
                headers[name] = value

        print(Fore.WHITE + f"\n[+] Testing with Origin: {test_origin}")

        try:
            response = requests.request(method, url, headers=headers)

            if response.status_code == 404 and ignore_404 == False:
                print(Fore.YELLOW + f"\nThe URL {url} returned a 404 Not Found. Exiting.")
                return

            print(Fore.CYAN + "Request Headers:")
            print(json.dumps(dict(response.request.headers), indent=2))

            print(Fore.CYAN + "\nResponse Headers:")
            print(json.dumps(dict(response.headers), indent=2))
            
            allow_origin = response.headers.get('Access-Control-Allow-Origin')
            allow_credentials = response.headers.get('Access-Control-Allow-Credentials')

            if not allow_origin:
                print(Fore.GREEN + "\nNo CORS headers found. Not vulnerable.")
                continue

            if allow_origin == "*":
                print(Fore.RED + "\nVulnerable! Found header Access-Control-Allow-Origin with value '*'.")
                if allow_credentials == 'true':
                    print(Fore.RED + "Especially dangerous! Found header Access-Control-Allow-Credentials with value 'true'.")
                continue

            if allow_origin == headers['Origin']:
                print(Fore.RED + "\nVulnerable! Access-Control-Allow-Origin header reflects the provided Origin.")
                if allow_credentials == 'true':
                    print(Fore.RED + "Especially dangerous! Found header Access-Control-Allow-Credentials with value 'true'.")
                continue

            print(Fore.GREEN + "\nNot vulnerable to simple CORS misconfigurations. Consider further testing with different origins.")

        except requests.RequestException as e:
            print(Fore.RED + f"\nFailed to send request to {url}. Error: {e}")
