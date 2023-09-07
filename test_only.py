import requests
from colorama import Fore
import json

def check_cors_vulnerability(url, url_list, method="GET", headers_list=None,origins_list=None, ignore_404=False, verbose=False):
    if url:
        base_domain = url.split("//")[-1].split("/")[0]
        test_cors(url,base_domain,method,headers_list,origins_list,ignore_404,verbose)
    if url_list:
        with open(url_list, 'r') as f:
            for url in f:
                url = url.strip()
                base_domain = url.split("//")[-1].split("/")[0]
                test_cors(url,base_domain,method,headers_list,origins_list,ignore_404,verbose)

def test_cors(url,base_domain,method,headers_list,origins_list,ignore_404,verbose):

    test_origins = [
        f"http://{base_domain}",
        "https://malicious.com",
        "http://malicious.com",
        f"http://sub.{base_domain}",
        f"https://sub.{base_domain}"
    ]

    if origins_list:
        test_origins = []
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
        print(Fore.WHITE + f"[+] Testing URL: {url}")
        print(Fore.WHITE + f"[+] Testing with Origin: {test_origin}")

        try:
            response = requests.request(method, url, headers=headers)

            if response.status_code == 404 and ignore_404 == False:
                print(Fore.YELLOW + f"\nThe URL {url} returned a 404 Not Found. Exiting.")
                return

            if verbose == True:
                print(Fore.CYAN + "\nRequest Headers:")
                print(json.dumps(dict(response.request.headers), indent=2))
                print(Fore.CYAN + "\nResponse Headers:")
                print(json.dumps(dict(response.headers), indent=2))

            allow_origin = response.headers.get('Access-Control-Allow-Origin')
            allow_credentials = response.headers.get('Access-Control-Allow-Credentials')

            if not allow_origin:
                print(Fore.GREEN + "\nNo CORS headers found. Not vulnerable.\n")
                continue

            if allow_origin == "*":
                print(Fore.RED + "\nVulnerable! Found header Access-Control-Allow-Origin with value '*'.")
                if allow_credentials == 'true':
                    print(Fore.RED + "Especially dangerous! Found header Access-Control-Allow-Credentials with value 'true'.\n")
                continue

            if allow_origin == headers['Origin']:
                print(Fore.RED + "\nVulnerable! Access-Control-Allow-Origin header reflects the provided Origin.")
                if allow_credentials == 'true':
                    print(Fore.RED + "Especially dangerous! Found header Access-Control-Allow-Credentials with value 'true'.\n")
                continue

            print(Fore.GREEN + "\nNot vulnerable to simple CORS misconfigurations. Consider further testing with different origins.")

        except requests.RequestException as e:
            print(Fore.RED + f"\nFailed to send request to {url}. Error: {e}\n")
