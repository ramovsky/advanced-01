import unittest

from fmw.commands import *


class Base(unittest.TestCase):

    def test_basic(self):
        p = Ping()
        print(p.to_bytes())

        pd = PingD(data='asdf1')
        print(pd.to_bytes())

        print(Packet.from_bytes(b'\x00\x00\x00\x01'))


if __name__ == '__main__':
    unittest.main()
