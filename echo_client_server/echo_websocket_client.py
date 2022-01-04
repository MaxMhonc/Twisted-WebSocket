# coding: utf8
import uuid
from autobahn.twisted.util import sleep
from autobahn.twisted.websocket import (
    WebSocketClientProtocol,
    WebSocketClientFactory
)
from twisted.internet.defer import Deferred, inlineCallbacks


class EchoClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        # Вывести IP-адрес сервера
        print(u"Server connected:{0}".format(response.peer))

    @inlineCallbacks
    def onOpen(self):
        print("WebSocket connection open.")

        # Посылать сообщения раз в секунду
        i = 0
        while True:
            # Послать текстовое сообщение.
            # Его НУЖНО закодировать вручную.
            self.sendMessage(u"© Hellø wørld{}!".format(i).encode('utf8'))
            # При отправке двоичных данных нужно сообщить об этом,
            # установив флаг "isBinary". Здесь мы создаем случайный
            # уникально-универсальный идентификатор и посылаем его
            # как последовательность байтов.
            self.sendMessage(uuid.uuid4().bytes, isBinary=True)
            i += 1
            yield sleep(1)

    def onMessage(self, payload, isBinary):
        # Не будем конвертировать сообщения, чтобы увидеть их
        # в исходной форме
        if isBinary:
            print(u"Binary message received:{!r}bytes".format(payload))
        else:
            print(u"Encoded text received:{!r}".format(payload))

    def onClose(self, wasClean, code, reason):
        print(u"WebSocket connection closed:{0}".format(reason))


if __name__ == '__main__':
    from twisted.internet import reactor

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = EchoClientProtocol
    reactor.connectTCP(u"127.0.0.1", 9000, factory)
    reactor.run()
