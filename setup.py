from setuptools import setup, find_packages

setup(name='web_crawler',
      version='0.1',
      description='Simple Web Crawler ',
      author='Akash Hiremath',
      author_email='akashh246@gmail.com',
      install_requires=[
          'requests',
          'BeautifulSoup'
      ],
      packages=find_packages())
