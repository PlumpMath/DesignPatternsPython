"""The main idea of Template Method is to create a method that will hold a
sequence of steps (primitive operations) for our algorithm to achieve some goal.
These primitive operations will be implemented in separate methods. Some
methods are the same for every kind of algorithm and some methods are different.
The same methods will be implemented in the abstract class, whereas,
the implementation of different methods will be in separate classes for
every kind of algorithm.

So, the sequence of steps to implement the Template Method is as follows:

    Create a method for the algorithm.
    Split the algorithm's implementation into several methods.
    Methods that are the same for every class should be implemented in the
    base class, whereas, specific methods should be implemented
    in the inherited class.
"""
from xml.dom import minidom
import urllib2 #to make http request to RSS and Atom feeds

class AbstractNewsParser(object):
    def __init__(self):
        #prohibit creating class instance
        if self.__class__ is AbstractNewsParser:
            raise TypeError('abstract class can  nott be instantiated')

    def print_top_news(self):
        """A template method - returns 3 latest news for every sites"""
        url = self.get_url()
        raw_content = self.get_raw_content(url)
        content = self.parse_content(raw_content)

        cropped = self.crop(content)

        for item in cropped:
            print 'Title: ', item['title']
            print 'Content: ', item['content']
            print 'Link: ', item['link']
            print 'Published: ', item['published']
            print 'Id: ', item['id']

    def get_url(self):
        raise NotImplementedError()

    def get_raw_content(self, url):
        return urllib2.urlopen(url).read()

    def parse_content(self, content):
        raise NotImplementedError()

    def crop(self, parsed_content, max_items=3):
        return parsed_content[:max_items]
#get_url, and parse is not implemented because it is specific to feed(rss/atom)

class YahooParser(AbstractNewsParser):
    def get_url(self):
        return 'http://news.yahoo.com/rss/'

    def parse_content(self, raw_content):
        parsed_content = []

        dom = minidom.parseString(raw_content)

        for node in dom.getElementsByTagName('item'):
            parsed_item = {}

            try:
                parsed_item['title'] = node.getElementsByTagName('title')\
                    [0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = None

            try:
                parsed_item['content'] = node.getElementsByTagName\
                    ('description')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['content'] = None

            try:
                parsed_item['link'] = node.getElementsByTagName\
                    ('link')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['link'] = None

            try:
                parsed_item['id'] = node.getElementsByTagName\
                    ('guid')[0].childNodes[0].nodeValue
            except:
                parsed_item['id'] = None

            try:
                parsed_item['published'] = node.getElementsByTagName\
                    ('pubDate')[0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['published'] = None

            parsed_content.append(parsed_item)
        return parsed_content


class GoogleParser(AbstractNewsParser):
    def get_url(self):
        return 'https://news.google.com/news/feeds?output=atom'

    def parse_content(self, raw_content):
        parsed_content = []

        dom = minidom.parseString(raw_content)

        for node in dom.getElementsByTagName('entry'):
            parsed_item = {}

            try:
                parsed_item['title'] = node.getElementsByTagName('title')\
                    [0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['title'] = None
            try:
                parsed_item['content'] = node.getElementsByTagName('content')\
                    [0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['content'] = None

            try:
                parsed_item['link'] = node.getElementsByTagName('link')\
                    [0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['link'] = None

            try:
                parsed_item['id'] = node.getElementsByTagName('id')\
                    [0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['id'] = None

            try:
                parsed_item['published'] = node.getElementsByTagName('updated')\
                    [0].childNodes[0].nodeValue
            except IndexError:
                parsed_item['published'] = None

            parsed_content.append(parsed_item)
        return parsed_content

if __name__ == '__main__':
    google = GoogleParser()
    yahoo = YahooParser()

    print 'Google: \n', google.print_top_news()
    print
    print 'Yahoo: \n', yahoo.print_top_news()

"""Summary....
The Template Method is a design pattern that defines the basis of an algorithm
and enables successors to redefine some steps of the algorithm without changing
its structure. The Template Method pattern allows good extensibility of the
algorithm, but only where permitted. This design pattern is well applied when
you have an algorithm whose behavior is common but the implementation may vary
and you have some steps that need to be adapted to different contexts.
"""
