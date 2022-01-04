from autobahn.twisted.websocket import (
    WebSocketServerProtocol,
    WebSocketServerFactory
)


class SignalingServerProtocol(WebSocketServerProtocol):
    connected_clients = []

    def onOpen(self):
        # Каждый раз, когда открывается очередное соединение WebSocket,
        # нужно сохранить ссылку на клиента в атрибуте класса, общем
        # для всех экземпляров протокола. Это упрощенная реализация, но
        # она прекрасно подходит для целей демонстрации.
        self.connected_clients.append(self)
        self.broadcast(str(len(self.connected_clients)))

    def broadcast(self, message):
        """ Посылает сообщение всем подключенным клиентам
        Параметры:
        message (str): посылаемое сообщение
        """

        for client in self.connected_clients:
            client.sendMessage(message.encode('utf8'))

    def onClose(self, wasClean, code, reason):
        # Если клиент отключился, ссылку на него нужно удалить из
        # атрибута класса.
        self.connected_clients.remove(self)
        self.broadcast(str(len(self.connected_clients)))


if __name__ == '__main__':
    from twisted.internet import reactor
    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = SignalingServerProtocol
    print(u"Listening on ws://127.0.0.1:9000")
    reactor.listenTCP(9000, factory)
    reactor.run()
