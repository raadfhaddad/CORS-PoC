import argparse
from ngrok_server import start_server,run_ngrok
from test_only import check_cors_vulnerability
from generate_html import load_template, generate_file

TOKEN = "123...XYZ" # ngrok token

def main():
    parser = argparse.ArgumentParser(description="Generate an HTML file to test CORS configurations.")
    subparsers = parser.add_subparsers(title="subcommands")

    parser_ngrok = subparsers.add_parser('ngrok', help="Generate HTML PoC file and run ngrok server")
    parser_ngrok.add_argument('--url', '-u', required=True, help="URL to test for CORS")
    parser_ngrok.add_argument('-H', '--header', action='append', help="Headers to set for the request. E.g. -H 'Cookie: a=a'")
    parser_ngrok.add_argument('-m', '--method', default='GET', help="HTTP method for the request. Default is GET.")
    parser_ngrok.set_defaults(func=lambda args: [generate_file(args.url, args.method, args.header), run_ngrok(TOKEN)]) 

    parser_html = subparsers.add_parser('html', help="Generate HTML PoC file")
    parser_html.add_argument('--url', '-u', required=True, help="URL to test for CORS")
    parser_html.add_argument('-H', '--header', action='append', help="Headers to set for the request. E.g. -H 'Cookie: a=a'")
    parser_html.add_argument('-m', '--method', default='GET', help="HTTP method for the request. Default is GET.")
    parser_html.set_defaults(func=lambda args: generate_file(args.url, args.method, args.header)) 
    

    parser_test = subparsers.add_parser('test', help="Test CORS misconfiguration")
    parser_test.add_argument('--url', '-u', required=True, help="URL to test for CORS misconfigurations")
    parser_test.add_argument('-m', '--method', default='GET', help="HTTP method for the test request. Default is GET.")
    parser_test.add_argument('-H', '--header', action='append', help="Headers to send with the test request. E.g. -H 'Cookie: a=a'")
    parser_test.add_argument('-o', '--origin', action='append', help="Add origin to be used in the Origins list. E.g. -o 'http://web.server'")
    parser_test.add_argument('-i', '--ignore404', action='store_true', help="Ignore 404 check")
    parser_test.set_defaults(func=lambda args: check_cors_vulnerability(args.url, args.method, args.header, args.origin, args.ignore404))  


    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)  
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
