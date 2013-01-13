import unittest

from protocol import *


class Base(unittest.TestCase):

    def test_lol(self):
        p = Ping()
        PingD(lol=1)
        print('types', p.__class__.types)


if __name__ == '__main__':
    unittest.main()
