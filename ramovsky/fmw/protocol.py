from collections import OrderedDict


class ImplemetatinoError(Exception): pass


class Field:
    type = NotImplemented

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if value.__class__ != self.type:
            raise ImplemetatinoError('Wrong type')
        setattr(instance, self.name, value)


class Cmd(Field):
    type = int


class Str(Field):
    type = str


class PacketMeta(type):

    types = {}

    def __init__(self, name, bases, dct):
        if dct.get('abstract'):
            return
        self.fields = OrderedDict()
        command = dct.pop('command')
        for k, v in dct.items():
            if not k.startswith('__'):
                self.fields[v.name] = v
        self.__class__.types[command] = self

    @classmethod
    def __prepare__(cls, name, base):
        return OrderedDict()


class PacketBase(metaclass=PacketMeta):

    abstract = True

    def __init__(self, **kw):
        pass

    @classmethod
    def create(bytes):
        pass


class Ping(PacketBase):

    command = 1


class PingD(PacketBase):

    command = 2



class Feeder:

    def __init__(self, connection):
        self.connection = connection
        self.buffer = []
        self.packet_length = None

    def feed(self):
        self.buffer += self.connection.recv(1024)
        if self.packet_length is None and len(self.buffer) > 2:
            self.packet_length = int.from_bytes(self.buffer[:2], byteorder='little')
            self.buffer = self.buffer[2:]
        if self.packet_length and self.packet_length <= len(self.buffer):
            return Packet(self.buffer[:self.packet_length])
