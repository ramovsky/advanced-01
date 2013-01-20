from .protocol import Packet, Cmd, Str

CONNECT = 1
CONNECTED = 2
PING = 3
PONG = 4
PINGD = 5
PONGD = 6
QUIT = 7
ACKQUIT = 8
FINISH = 9
ACKFINISH = 10

__all__ = (
    'Packet',
    'Connect',
    'Connected',
    'Ping',
    'Pong',
    'PingD',
    'PongD',
    'Quit',
    'AckQuit',
    'Finish',
    'AckFinish',
    )


class Connect(Packet):

    command = Cmd(CONNECT)

    def reply(self):
        return Pong().to_bytes()


class Connected(Packet):

    command = Cmd(CONNECTED)


class Ping(Packet):

    command = Cmd(PING)

    def reply(self):
        return Pong().to_bytes()


class Pong(Packet):

    command = Cmd(PONG)


class PingD(Packet):

    command = Cmd(PINGD)
    data = Str()

    def reply(self):
        return PongD(data=self.data).to_bytes()


class PongD(Packet):

    command = Cmd(PONGD)
    data = Str()


class Quit(Packet):

    command = Cmd(QUIT)

    def reply(self):
        return Ackquit().to_bytes()


class AckQuit(Packet):

    command = Cmd(ACKQUIT)


class Finish(Packet):

    command = Cmd(FINISH)

    def reply(self):
        return Ackfinish().to_bytes()


class AckFinish(Packet):

    command = Cmd(ACKFINISH)
