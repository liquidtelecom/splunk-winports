import unittest

from winports import split_ip_port


class TestSplitIpPort(unittest.TestCase):
    def test_ipv4(self):
        self.assertEqual(('192.168.0.1', '80'), split_ip_port('192.168.0.1:80'))

    def test_ipv6(self):
        self.assertEqual(('[fe80::251d:7f5c:b8a8:439e%13]', '546'), split_ip_port('[fe80::251d:7f5c:b8a8:439e%13]:546'))
        
    def test_stars(self):
        self.assertEqual(('*', '*'), split_ip_port('*:*'))


