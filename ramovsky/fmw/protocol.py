from collections import OrderedDict


__all__ = (
    'ImplemetatinoError',
    'Packet',
    )

class ImplemetatinoError(Exception): pass


class Field:
    type = NotImplemented

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value.__class__ != self.type:
            raise ImplemetatinoError('Wrong type')
        instance.__dict__[self.name] = value

    def __repr__(self):
        rep = str(self.__class__) + 'fields: '
        rep += ','.join('{}={}'.format(k, v) for k, v in self.__dict__.items())
        return rep

class Int(Field):
    type = int

    @staticmethod
    def to_bytes(value):
        return value.to_bytes(4, 'big')

    @staticmethod
    def from_bytes(value):
        return int.from_bytes(value[:4], 'big'), value[4:]


class Cmd(Int):
    type = int

    def __init__(self, id):
        self.__dict__['id'] = id


class Str(Field):
    type = str

    @staticmethod
    def to_bytes(value):
        return value.encode('utf-8')

    @staticmethod
    def from_bytes(value):
        return value.decode('utf-8')


class PacketMeta(type):

    types = {}

    def __init__(self, name, bases, dct):
        if dct.get('abstract'):
            return
        self._fields = OrderedDict()
        command = dct.get('command')
        if not isinstance(command, Cmd):
           raise ImplemetatinoError('Wrong command type')
        if command.id in self.__class__.types:
           raise ImplemetatinoError('Duplicated command id %s' % command)
        self.__class__.types[command.id] = self
        for k, v in dct.items():
            if isinstance(v, Field):
                v.name = k
                self._fields[k] = v

    @classmethod
    def __prepare__(cls, name, base):
        return OrderedDict()


class Packet(metaclass=PacketMeta):

    abstract = True

    def __init__(self, **kw):
        cmd, *fields = self._fields.keys()
        id = self._fields[cmd].id
        setattr(self, cmd, id)
        for field in fields:
            setattr(self, field, kw[field])

    @classmethod
    def from_bytes(cls, bytes):
        cmd, data = Int.from_bytes(bytes)
        packet_cls = cls.__class__.types[cmd]
        dct = {}
        for k, type in packet_cls._fields.items():
            val, bytes = type.from_bytes(bytes)
            dct[k] = val
        return packet_cls(**dct)

    def to_bytes(self):
        buf = b''
        for k, v in self._fields.items():
            buf += v.to_bytes(getattr(self, k))
        return Int.to_bytes(len(buf)) + buf



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
