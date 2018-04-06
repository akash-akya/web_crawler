import requests
import logging
import math
from bs4 import BeautifulSoup as Soup
from urllib import parse as parse
from collections import OrderedDict

class Crawler(object):
    """ 
    Crawls the urls passed keeping the pages url in url_repo 
    """
    url_repo = OrderedDict()

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def __clean_url(self, url):
        return parse.urldefrag(url)[0]

    def __is_valid_url(self, url):
        try:
            result = parse.urlparse(url)
            return result.scheme and result.netloc and result.scheme in ('http', 'https')
        except:
            return False

    def __get_links(self, req_url):
        r = requests.get(req_url)
        html = Soup(r.content, 'html.parser')
        return [req_url] + [parse.urljoin(req_url, a.get('href')) for a in html.find_all('a')]

    def get_url(self, index):
        i = 0
        for url in self.url_repo:
            if i == index: return url
            i += 1
        return None

    def get_url_count(self):
        return len(self.url_repo)

    def crawl(self, url, count=math.inf):
        url = self.__clean_url(url)
        self.logger.info("Crawling: "+url)

        links = self.__get_links(url)
        i = 0
        for link in links:
            if i >= count: break
            u = self.__clean_url(link)
            if self.__is_valid_url(u):
                if u not in self.url_repo:
                    self.url_repo[u] = True
                    i += 1
            else:
                self.logger.warn('Invalid url: %s', u)

    def print(self):
        for link in self.url_repo:
            print(link)
