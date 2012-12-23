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
