import requests
import logging
import math
from bs4 import BeautifulSoup as Soup
from urllib import parse as parse
from collections import OrderedDict

class Crawler(object):
    """ 
    Crawlers Class maintains internal queue of parsed urls
    and crawls based on request 
    """

    # Since lookup of url to check its present or not needs to be done several times, and
    # order of the URLs needs to be maintained, using OrderedDict. (Ordered Set can be used too)
    url_repo = OrderedDict()

    def __init__(self, logger=None):
        """
        Initialize the logger if passed else create one
        """
        self.logger = logger or logging.getLogger(__name__)

    def __clean_url(self, url):
        """
        Remove framents present in the URL, Since multiple URL with
        differing only Fragment ID need not be visited twice.

        Ex: Follwing all refers to same page, Don't visit them multiple times
            http://something.com/index.html
            http://something.com/index.html#node2
            http://something.com/index.html#someting
        """
        return parse.urldefrag(url)[0]

    def __is_valid_url(self, url):
        """
        Return True only if the URL is using http/https scheme
        and have hostname
        """
        try:
            result = parse.urlparse(url)
            return result.scheme and result.netloc and result.scheme in ('http', 'https')
        except:
            return False

    def __get_links(self, req_url):
        """
        Get the body of the URL, parse it, 
        then get all 'Anchor' tags links with absolute path
        """
        r = requests.get(req_url, timeout=5)
        html = Soup(r.content, 'html.parser')
        return [req_url] + [parse.urljoin(req_url, a.get('href')) for a in html.find_all('a')]


    ##### PUBLIC METHODS #####
    def get_url(self, index):
        """
        Return ith URL from the repo
        """
        i = 0
        for url in self.url_repo:
            if i == index: return url
            i += 1
        return None

    def get_url_count(self):
        return len(self.url_repo)

    def crawl(self, url, count=math.inf):
        """
        Visits the URL passed and appends the URLs found in that page.
        count is the number of urls need to be appended. Default Inifinity ie. All
        """
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

    def print_urls(self):
        """
        Print the URLs in the repo with formatting
        """
        print('\n--------------------------------------------')
        print(' URLS IN THE REPO')
        print('--------------------------------------------\n')
        for url in self.url_repo:
            print(url)
        print('\n Total urls count: {}\n'.format(len(self.url_repo)))

