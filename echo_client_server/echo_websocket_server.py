import uuid
from autobahn.twisted.websocket import (
    WebSocketServerProtocol,
    WebSocketServerFactory
)


class EchoServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        """Вызывается при подключении клиента"""
        # Вывести IP-адрес клиента, обслуживаемого этим экземпляром протокола
        print(u"Client connecting:{0}".format(request.peer))

    def onOpen(self):
        """Вызывается при открытии соединения WebSocket"""
        print(u"WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        """Вызывается при получении очередного сообщения от клиента
        Параметры:
        payload (str|bytes): содержимое сообщения
        isBinary (bool): содержит ли сообщение кодированный текст (False)
        или двоичные данные (True). Значение по умолчанию False.
        """

        # Просто вывести полученное сообщение
        if isBinary:
            # Это двоичное сообщение и может содержать любые байты.
            # Здесь мы воссоздаем UUID из байтов, полученных от клиента.
            uid = uuid.UUID(bytes=payload)
            print(u"UUID received:{}".format(uid))
        else:
            # Это кодированный текст. Обратите внимание, что он НЕ
            # декодируется автоматически, isBinary – это просто флаг, который
            # клиент любезно устанавливает для каждого сообщения. Вы должны
            # знать, какой набор символов используется (здесь utf8), и вызвать
            # ".decode()", чтобы преобразовать байты в строковый объект.
            print(u"Text message received:{}".format(payload.decode( 'utf8')))

        # Это -- эхо-сервер, поэтому отправим обратно все, что получили
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        """Вызывается при закрытии соединения WebSocket клиентом
        Параметры:
        wasClean (bool): соединение только будет закрыто, или это уже произошло.
        code (int): любой код из коллекции WebSocketClientProtocol.CLOSE_*
        reason (str): простое текстовое сообщение, описывающее причину
        закрытия соединения
        """

        print(u"WebSocket connection closed:{0}".format(reason))


if __name__ == '__main__':
    from twisted.internet import reactor
    # В качестве схемы протокол WebSocket использует WS. Поэтому WebSocket URL
    # выглядит точно так же, как HTTP URL, но со схемой WS вместо HTTP.
    factory=WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol=EchoServerProtocol
    print(u"Listening on ws://127.0.0.1:9000")
    reactor.listenTCP(9000, factory)
    reactor.run()
    