import unittest

from fmw.commands import *


class Base(unittest.TestCase):

    def test_to_bytes(self):
        p1 = Connect()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x01', p1.to_bytes())

        p2 = Connected()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x02', p2.to_bytes())
        self.assertEqual(p1.reply(), p2.to_bytes())

        p1 = Ping()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x03', p1.to_bytes())

        p2 = Pong()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x04', p2.to_bytes())
        self.assertEqual(p1.reply(), p2.to_bytes())

        p1 = PingD(data='data')
        self.assertEqual(b'\x00\x00\x00\x08\x00\x00\x00\x05data', p1.to_bytes())

        p2 = PongD(data='data')
        self.assertEqual(b'\x00\x00\x00\x08\x00\x00\x00\x06data', p2.to_bytes())
        self.assertEqual(p1.reply(), p2.to_bytes())

        p1 = Quit()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x07', p1.to_bytes())

        p2 = AckQuit()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x08', p2.to_bytes())
        self.assertEqual(p1.reply(), p2.to_bytes())

        p1 = Finish()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x09', p1.to_bytes())

        p2 = AckFinish()
        self.assertEqual(b'\x00\x00\x00\x04\x00\x00\x00\x0a', p2.to_bytes())
        self.assertEqual(p1.reply(), p2.to_bytes())

    def test_from_bytes(self):
        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x01'),
            Connect())

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x02'),
            Connected())

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x03'),
            Ping())

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x04'),
            Pong())

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x05data'),
            PingD(data='data'))

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x06data'),
            PongD(data='data'))

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x07'),
            Quit())

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x08'),
            AckQuit())

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x09'),
            Finish())

        self.assertEqual(
            Packet.from_bytes(b'\x00\x00\x00\x0a'),
            AckFinish())


if __name__ == '__main__':
    unittest.main()
