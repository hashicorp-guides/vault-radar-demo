import os

from config import DEBUG


def save_debug_info(folder, name, response):
    if DEBUG:
        if not os.path.exists(f"{folder}"):
            os.makedirs(f"{folder}")

        with open(f"{folder}/{name}-content.html", "w") as file:
            file.write(response.content.decode("utf-8"))

        with open(f"{folder}/{name}-text.txt", "w") as file:
            file.write(response.text)

        with open(f"{folder}/{name}-headers.txt", "w") as file:
            file.write(str(response.headers))


def translate_to_curl(response):
    if DEBUG:
        req = response.request
        command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        method, uri, data = req.method, req.url, req.body
        headers = ["'{0}: {1}'".format(k, v) for k, v in req.headers.items()]
        headers = " -H ".join(headers)
        print(f'cURL equivalent of request: {command.format(method=method, headers=headers, data=data, uri=uri)}')
