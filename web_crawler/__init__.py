import crawler
from crawler import Crawler
import signal
import logging
import requests
import logging.config
import sys

logging.config.fileConfig('../config/logging.ini')
logger = logging.getLogger('Init')

if __name__ == '__main__':
    try:
        url = sys.argv[1]
        limit = int(sys.argv[2])
    except:
        print('Invalid arguments')
        print('Usage:\n    python3 __init__.py <url> <count>')
        sys.exit(1)

    try:
        c = Crawler(logging.getLogger('Crawler'))
        
        try:
            c.crawl(url, limit)
        except requests.exceptions.RequestException as requestsError:
            logger.error(
                'Failed to get the response for url: %s\nError:%s', url, requestsError)

        i = 0
        while c.get_url_count() < limit and i < c.get_url_count():
            try:
                c.crawl(c.get_url(i), limit-c.get_url_count())
            except requests.exceptions.RequestException as requestsError:
                logger.error(
                    'Failed to get the response for url: %s\nError:%s', url, requestsError)
            i += 1

    except KeyboardInterrupt:
        logger.info('Interrupted. Stopping crawling')

    c.print()
