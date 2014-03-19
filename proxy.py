import asyncore
import socket


class ResponseHandler(asyncore.dispatcher):
    def __init__(self, sock, data):
        asyncore.dispatcher.__init__(self)
        self.sock = sock
        self.sock.send(data)


class HttpClient(asyncore.dispatcher):
    def __init__(self, sock, host, data):
        asyncore.dispatcher.__init__(self)
        self.sock = sock
        self.data = data
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 80))

    def handle_connect(self):
        self.send(self.data)

    def handle_read(self):
        data = self.recv(8192)
        if data:
            ResponseHandler(self.sock, data)


class RequestHandler(asyncore.dispatcher):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            pos = data.find(b'\r\n\r\n')
            src_headers = data[:pos]
            headers = src_headers.split(b'\r\n')
            method, url, http_version = headers[0].split(b' ')
            header = dict((x[:x.find(b':')].lower(), x[x.find(b':')+1:].strip()) for x in headers[1:])
            HttpClient(self, header[b'host'], data)


class ProxyServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from {0}'.format(repr(addr)))
            RequestHandler(sock)


if __name__ == '__main__':
    server = ProxyServer('localhost', 8080)
    asyncore.loop()