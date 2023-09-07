# CORS-PoC
CORS-PoC: Python tool for bug bounty hunters and penetration testers to detect CORS misconfigurations, generating PoC and integrating with ngrok for easy validation.
## Usage/Examples
The tool comes with three options to choose from {**ngrok,html,test**}
```
usage: tool.py [-h] {ngrok,html,test} ...

Generate an HTML file to test CORS configurations.

options:
  -h, --help         show this help message and exit

subcommands:
  {ngrok,html,test}
    ngrok            Generate HTML PoC file and run ngrok server
    html             Generate HTML PoC file
    test             Test CORS misconfiguration
```

### Test CORS:
#### [+] Test CORS configurations based on server's response headers:
```
python3 tool.py test -u http://localhost/ -m GET -H "Cookie: sessionid=123"
```
#### [+] Add Origins of your choice to the Origins list
```
python3 tool.py test -u http://localhost/ -m GET -H "Cookie: sessionid=123" -o http://localhost.xyz/
```
#### [+] Ignore 404 check
```
python3 tool.py test -u http://localhost/ -m GET -H "Cookie: sessionid=123" -o http://localhost.xyz/ -i
```
### Generate PoC File:
```
python3 tool.py html -u http://localhost/ -m GET -H "Project-Id: 123"
```
* You can find the generated HTML file inside **output** directory
#### Generate PoC File and test with ngrok
> Make sure to update your token in **tool.py** file to integrate **ngrok**
```
python3 tool.py ngrok -u http://localhost/ -m GET -H "Project-Id: 123"
```
* **ngrok** public link that points to a temperory local server will appear in the terminal
```
...
Public URL: NgrokTunnel: "https://12-34-56-78-90.ngrok-free.app" -> "http://localhost:8000"
...
```
## Demo
<img width="697" alt="Screenshot 2023-09-07 at 20 47 07" src="https://github.com/raadfhaddad/CORS-PoC/assets/13183963/a10ef1f4-6d96-4035-8a1a-f39a8b1a3b83">
<img width="764" alt="Screenshot 2023-09-07 at 20 51 45" src="https://github.com/raadfhaddad/CORS-PoC/assets/13183963/da537bbc-bd79-473b-a58d-14e0dfaa6526">


```NOTE: The tool was created with the support of the amazing tool ChatGPT!```
