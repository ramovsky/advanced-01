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
        instance.__dict__[self.name] = value


class Cmd(Field):
    type = int

    def __init__(self, id):
        self.id = id


class Str(Field):
    type = str


class PacketMeta(type):

    types = {}

    def __init__(self, name, bases, dct):
        if dct.get('abstract'):
            return
        self._fields = OrderedDict()
        command = dct.pop('command')
        if not isinstance(command, Cmd):
           raise ImplemetatinoError('Wrong command type')
        if command.id in self.__class__.types:
           raise ImplemetatinoError('Duplicated command id %d' % command)
        self.__class__.types[command.id] = self
        for k, v in dct.items():
            if isinstance(v, Field):
                v.name = k
                self._fields[k] = v

    @classmethod
    def __prepare__(cls, name, base):
        return OrderedDict()


class PacketBase(metaclass=PacketMeta):

    abstract = True

    def __init__(self, **kw):
        for name, field in self._fields.items():
            field.__set__(self, kw[name])

    @classmethod
    def from_bytes(bytes):
        pass

    def to_bytes(self):
        for k, v in self._fields.items():
            print('vals', k, v)



class Ping(PacketBase):

    command = Cmd(1)


class PingD(PacketBase):

    command = Cmd(2)
    data = Str()


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
