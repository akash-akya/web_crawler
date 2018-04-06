
# web_crawler
Simple implementation of Web Crawler. Fetches the URLs present web pages recursively in a sequential order utill its interrupted with `Ctrl+c` or meets the **maximum limit** provided. Prints the URLs present in the repository at the end.



## Requirement
Python 3.5+


[Requests](http://docs.python-requests.org/en/master/)


[BeautifulSoap](https://www.crummy.com/software/BeautifulSoup/)

## Usage

    $ python3 __main__.py <url> <count> ?<delay>

- **url**  seed url from which crawling should start
- **count** Maximum number of urls to be collected
- **delay** Delay between the requests to avoid overloading the server (Optional)




## Limitation



- Works only for http & https scheme, ignores the rest
- Doesn't work for dynamic websites , like websites with infinite scrolling or Sites which load
s the content based on some js code
- Not parallel, Requests runs sequentially 






