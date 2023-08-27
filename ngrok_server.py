import http.server
import os
from pyngrok import ngrok

def start_server(authtoken=None):
    if authtoken:
        ngrok.set_auth_token(authtoken)

    DIRECTORY_TO_SERVE = 'output'
    os.chdir(DIRECTORY_TO_SERVE)

    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    httpd = http.server.HTTPServer(("", PORT), Handler)

    public_url = ngrok.connect(PORT)
    print(f"Public URL: {public_url}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        ngrok.disconnect(public_url)

def run_ngrok(token):
    start_server(authtoken=token)
