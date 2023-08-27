def load_template(filename):
    with open(filename, 'r') as file:
        return file.read()

def generate_file(url, method, headers):
    
    template = load_template("templates/cors-test.html")
    
    updated_content = template.replace('{url}', url).replace('{method}', method)
    
    headers_str = ""
    if headers:
        header_entries = []
        for header in headers:
            name, value = header.split(":", 1)
            header_entries.append(f"\"{name}\": \"{value}\"")
        headers_str = ",".join(header_entries)
        updated_content = updated_content.replace("/*{{headers}}*/", headers_str)
    
    with open("output/index.html", "w") as file:
        file.write(updated_content)

    print("Generated index.html for testing CORS with the URL:", url)
