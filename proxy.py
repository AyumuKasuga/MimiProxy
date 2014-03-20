import asyncio


class HttpClient(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.server_transport.write(data)


class ProxyServer(asyncio.Protocol):

    @asyncio.coroutine
    def parse_request(self, data):
        pos = data.find(b'\r\n\r\n')
        src_headers = data[:pos]
        headers = src_headers.split(b'\r\n')
        method, url, http_version = headers[0].split(b' ')
        header = dict((x[:x.find(b':')].lower(), x[x.find(b':')+1:].strip()) for x in headers[1:])
        print(header[b'host'])
        protocol, client = yield from asyncio.get_event_loop().create_connection(HttpClient, header[b'host'], 80)
        client.server_transport = self.transport
        client.transport.write(data)

    def connection_made(self, transport):
        self.transport = transport


    def data_received(self, data):
        asyncio.Task(self.parse_request(data))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    coro = loop.create_server(ProxyServer, '127.0.0.1', 8080)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit")
    finally:
        server.close()
        loop.close()