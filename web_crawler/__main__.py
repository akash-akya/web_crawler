from web_crawler.crawler import Crawler
import os
import time
import signal
import logging
import requests
import logging.config
import sys

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config/logging.ini')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('Init')

def print_error(err):
    """
    prints the formatted logger error msg and prints on stdout 
    based on the 'Error' passed
    """
    logger.error('Failed to make a request for \
                        \n\tURL: %s \n\tError: %s\n\tDesc: %s', url, type(err).__name__, err)
    print('Error: '+type(err).__name__)

usage_msg = """\nSimple Web Crawler
        \nUsage:\tpython3 __main__.py <url> <count> ?<delay>
    url:   Seed url from which crawling should start
    count: Maximum number of urls to be collected
    delay: Delay between the requests (Optional)"""

if __name__ == '__main__':
    # Parse arguments. URL, limit are madatory. delay is optional.
    # Otherwise exit with usage_msg
    try:
        url = sys.argv[1]
        limit = int(sys.argv[2])
        # Delay to avoid overloading the server. If not passed no delay
        delay = int(sys.argv[3]) if len(sys.argv) == 4 else 0
    except:
        print('Invalid arguments!')
        print(usage_msg)
        sys.exit(1)

    try:
        c = Crawler(logging.getLogger('Crawler'))
        # Maximum failure limit to avoid execessive error logging
        MAX_ERROR_RETRY, error_count = 5, 0
        
        try:
            c.crawl(url, limit)
        except requests.RequestException as err:
            print_error(err)
            error_count += 1

        # Crawl URLs present in the Crawler Queue sequentially
        i = 1
        while i < c.get_url_count() and c.get_url_count() < limit:
            try:
                time.sleep(delay)
                c.crawl(c.get_url(i), limit-c.get_url_count())
            except requests.RequestException as err:
                print_error(err)
                error_count += 1
                # If error limit is reached, try no more
                if error_count == MAX_ERROR_RETRY: break
            i += 1
    # Handle Ctrl+c interrupt
    except KeyboardInterrupt:
        logger.info('Interrupted. Stop crawling')

    # Print the URLs with formatting
    c.print_urls()
