import unittest

from protocol import *


class Base(unittest.TestCase):

    def test_lol(self):
        p = Ping()
        pd = PingD(data='1', command=4)
        pd.to_bytes()


if __name__ == '__main__':
    unittest.main()
