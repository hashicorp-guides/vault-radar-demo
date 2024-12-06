import os

from config import DEBUG


def save_debug_info(folder, name, response):
    if DEBUG:
        if not os.path.exists(f"{folder}"):
            os.makedirs(f"{folder}")

        file = open(f"{folder}/{name}-content.html", "w")
        file.write(response.content.decode("utf-8"))
        file.close()

        file = open(f"{folder}/{name}-text.txt", "w")
        file.write(response.text)
        file.close()

        file = open(f"{folder}/{name}-headers.txt", "w")
        file.write(str(response.headers))
        file.close()


def translate_to_curl(response):
    if DEBUG:
        req = response.request
        command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        method, uri, data = req.method, req.url, req.body
        headers = ["'{0}: {1}'".format(k, v) for k, v in req.headers.items()]
        headers = " -H ".join(headers)
        print(f'cURL equivalent of request: {command.format(method=method, headers=headers, data=data, uri=uri)}')
