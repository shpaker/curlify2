class Curlify:
    def __init__(self, request, compressed=False, verify=True):
        self.req = request
        self.compressed = compressed
        self.verify = verify

    def to_curl(self) -> str:
        """to_curl function returns a string of curl to execute in shell.
        We accept 'requests' and 'httpx' module.
        """
        return self.quote()

    def headers(self) -> str:
        """organize headers

        Returns:
            str: return string of set headers
        """
        headers = " -H ".join([f'"{k}: {v}"' for k, v in self.req.headers.items()])
        if headers:
            headers = f"-H {headers}"
        return headers

    def body(self):
        if hasattr(self.req, "body"):
            return self.req.body

        return self.req.read()

    def body_decode(self):
        body = self.body()

        if body and isinstance(body, bytes):
            return body.decode()

        return body

    def make_curl_cli(self, method, headers, body):
        cli_parts = [
            f"curl -X {method}",
            headers,
            f"-d '{body}'" if body else None,
            self.req.url,
        ]
        quote = ' '.join([str(entity) for entity in cli_parts if entity])

        if self.compressed:
            quote += " --compressed"
        if not self.verify:
            quote += " --insecure"
        return quote

    def quote(self) -> str:
        """build curl command

        Returns:
            str: string represents curl command
        """
        return self.make_curl_cli(self.req.method, self.headers(), self.body_decode())


class AsyncCurlify(Curlify):

    async def to_curl(self) -> str:
        """to_curl function returns a string of curl to execute in shell.
        We accept 'requests' and 'httpx' module.
        """
        return await self.quote()

    async def body(self):
        if hasattr(self.req, "body"):
            return self.req.body

        return await self.req.aread()

    async def body_decode(self):
        body = await self.body()

        if body and isinstance(body, bytes):
            return body.decode()

        return body

    async def quote(self) -> str:
        """build curl command

        Returns:
            str: string represents curl command
        """
        body = await self.body_decode()
        return self.make_curl_cli(self.req.method, self.headers(), body)
