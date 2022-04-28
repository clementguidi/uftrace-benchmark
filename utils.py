import requests


def url_parse_filename(url):
    try:
        pos = url.rindex("/")
    except ValueError as err:
        print(f"No filename in url: {err}")
        exit(1)

    pos += 1
    name = url[pos::]
    return name

def http_get(url, of=""):
    if of == "":
        of = url_parse_filename(url)
    data = requests.get(url)
    with open(of, "wb") as file:
        print(f"DOWNLOAD {url} to {of}")
        file.write(data.content)
