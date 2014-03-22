import asyncio
from struct import unpack, pack


class Client(asyncio.Protocol):
    pass


class ProxyServer(asyncio.Protocol):

    STAGE_HELLO = 1
    STAGE_AUTH = 2
    STAGE_WORK = 3

    CMD_CONNECT = 1
    CMD_BIND = 2
    CMD_UDP_ASSOCIATE = 3

    ATYP_IPV4 = 1
    ATYP_DOMAIN = 3
    ATYP_IPV6 = 4

    def connection_made(self, transport):
        self.stage = self.STAGE_HELLO
        self.transport = transport

    def data_received(self, data):
        if self.stage == self.STAGE_HELLO:
            print('hello')
            ver, nmethods = unpack(b'bb', data[:2])
            methods = unpack(nmethods * b'b', data[2:])
            self.transport.write(pack(b'bb', 5, 0))
            self.stage = self.STAGE_WORK
        elif self.stage == self.STAGE_AUTH:
            print('auth')
        elif self.stage == self.STAGE_WORK:
            print('work')
            ver, cmd, rsv, atyp = unpack(b'bbbb', data[:4])
            print(ver, cmd, rsv, atyp)
            print(unpack(b'!H', data[-2:]))
            if atyp == self.ATYP_IPV4:
                print(unpack(b'BBBB', data[4:8]))

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