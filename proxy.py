import asyncio
from struct import unpack, pack


class Client(asyncio.Protocol):

    def connection_made(self, transport):
        self.server_transport = None
        self.transport = transport

    def data_received(self, data):
        self.server_transport.write(data)


    def connection_lost(self, exc):
        self.server_transport.close()

class ProxyServer(asyncio.Protocol):

    STAGE_HELLO = 1
    STAGE_AUTH = 2
    STAGE_INIT = 3
    STAGE_WORK = 4

    CMD_CONNECT = 1
    CMD_BIND = 2
    CMD_UDP_ASSOCIATE = 3

    ATYP_IPV4 = 1
    ATYP_DOMAIN = 3
    ATYP_IPV6 = 4

    @asyncio.coroutine
    def request_init(self, address, port):
        _, self.client = yield from asyncio.get_event_loop().create_connection(Client, address, port)
        self.client.server_transport = self.transport
        client_address, client_port = self.client.transport.get_extra_info('peername')
        client_addr_port = [int(x) for x in client_address.split('.')]
        client_addr_port.append(client_port)
        resp = pack(b'bbbbBBBBH', 5, 0, 0, self.ATYP_IPV4, *client_addr_port)
        self.transport.write(resp)

    @asyncio.coroutine
    def request(self, data):
        self.client.transport.write(data)

    def connection_made(self, transport):
        self.stage = self.STAGE_HELLO
        self.transport = transport

    def data_received(self, data):
        print(self.transport.get_extra_info('peername'))
        if self.stage == self.STAGE_HELLO:
            ver, nmethods = unpack(b'bb', data[:2])
            methods = unpack(nmethods * b'b', data[2:])
            self.transport.write(pack(b'bb', 5, 0))
            self.stage = self.STAGE_INIT
        elif self.stage == self.STAGE_AUTH:
            pass
        elif self.stage == self.STAGE_INIT:
            ver, cmd, rsv, atyp = unpack(b'bbbb', data[:4])
            self.port = unpack(b'!H', data[-2:])[0]
            if atyp == self.ATYP_IPV4:
                self.address = '.'.join([str(x) for x in unpack(b'BBBB', data[4:8])])
                self.stage = self.STAGE_WORK
                asyncio.async(self.request_init(self.address, self.port))
            elif atyp == self.ATYP_IPV6:
                # not implemented yet
                resp = pack(b'bbbbBBBBH', 5, 8, 0, self.ATYP_IPV4, 127, 0, 0, 1, 8080)
                self.transport.write(resp)
                self.transport.close()
            elif atyp == self.ATYP_DOMAIN:
                # not implemented yet
                resp = pack(b'bbbbBBBBH', 5, 8, 0, self.ATYP_IPV4, 127, 0, 0, 1, 8080)
                self.transport.write(resp)
                self.transport.close()
        else:
            print('work')
            asyncio.async(self.request(data))



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