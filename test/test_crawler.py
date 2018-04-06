import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../web_crawler/')))

import unittest
import requests
from crawler import Crawler

class TestCrawler(unittest.TestCase):
    """
    Our basic test class
    """

    def test_invalid_url(self):
        """
        The actual test.
        """
        c = Crawler()
        self.assertRaises(requests.exceptions.InvalidSchema, c.crawl,
                          'httxp://clhs.lisp.se/Body/f_countc.htm', 10)

    def test_defragmention(self):
        """
        The actual test.
        """
        c = Crawler()
        c.crawl('http://clhs.lisp.se/Body/f_countc.htm', 10)
        self.assertEqual(False, '#' in c.get_url(9))

    def test_url_validation(self):
        """
        The actual test.
        """
        c = Crawler()
        self.assertEqual(False, c._Crawler__is_valid_url(
            'ftp://clhs.lisp.se/Body/f_countc.htm'))

    def test_get_links(self):
        """
        The actual test.
        """
        c = Crawler()
        self.assertEqual(61, len(c._Crawler__get_links(
            'http://clhs.lisp.se/Body/f_countc.htm')))

    def test_get_url(self):
        """
        The actual test.
        """
        c = Crawler()
        c.crawl('http://clhs.lisp.se/Body/f_countc.htm')
        self.assertEqual('http://www.lispworks.com/', c.get_url(1))

if __name__ == '__main__':
    unittest.main()
