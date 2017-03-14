"""
Abstract Factory is used when you need to create a family of objects that
do some work together.

The benefit of using Abstract Factory is that it isolates the creation of
objects from the client that needs them, giving the client only the possibility
of accessing them through an interface, which makes the manipulation easier.
If the products of a family are meant to work together, the AbstractFactory
class makes it easy to use the objects from only one family at a time. On the
other hand, adding new products to the existing factories is difficult because
the AbstractFactory interface uses a fixed set of products that can be created.
This is why adding a new product would mean extending the factory interface,
which involves changes in the AbstractFactory class and all its subclasses:
"""
import abc
import urllib2
from BeautifulSoup import BeautifulStoneSoup


class AbstractFactory(object):
    """AbstractFactory interface provides 3 methods to implement in its
    sublcasses: create_protocol, create_port, and create_parser"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure

    @abc.abstractmethod
    def create_protocol(self):
        pass

    @abc.abstractmethod
    def create_port(self):
        pass

    @abc.abstractmethod
    def create_parser(self):
        pass


#HTTPFactory class creates its family of realted objects
class HTTPFactory(AbstractFactory):
    """Concrete factory for building HTTP connection"""

    def create_protocol(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def create_port(self):
        if self.is_secure:
            return HTTPSecurePort()
        return HTTPPort()

    def create_parser(self):
        return HTTPParser()

class FTPFactory(AbstractFactory):
    """Concrete factory for building FTP connection"""

    def create_protocol(self):
        return 'ftp'

    def create_port(self):
        return FTPPort()

    def create_parser(self):
        return FTPParser()

#Implementation of products classes Port and Parser
class Port(object):
    __metaclass__ = abc.ABCMeta
    """An abstract prodcut - represents port to connect"""
    @abc.abstractmethod
    def __str__(self):
        pass

class HTTPPort(Port):
    """A concret product - http port"""
    def __str__(self):
        return '80'

class HTTPSecurePort(Port):
    def __str__(self):
        return '443'

class FTPPort(Port):
    def __str__(self):
        return '21'

class Parser(object):
    """An abstract product - parser to parse web content"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, content):
        pass

class HTTPParser(Parser):
    def __call__(self, content):
        filenames = []
        soup = BeautifulStoneSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(link.text)
        return '\n'.join(filenames)

class FTPParser(Parser):
    def __call__(self, content):
        lines = content.split('\n')
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)

#Connector is a class that accetps a factory, and this factory is used to inject
#the components protocol, port, and the moethod to parse
class Connector(object):
    """A client"""
    def __init__(self, factory):
        """factory is an AbstractFactory instance"""
        self.protocol = factory.create_protocol()
        self.port = factory.create_port()
        self.parse = factory.create_parser()

    def read(self, host, path):
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print "Connecting to ", url
        return urllib2.urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def parse(self):
        pass

#in the runtime, client determines which factory to use, creates the factory,
#and instantiates the connector passing the factory
#read method is called after that and parsed it
if __name__ == '__main__':
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD/'
    protocol = input('Connecting to {}. Which protocol to use? (0-http, 1-ftp)\
                     : '.format(domain))

    if protocol == 0:
        is_secure = bool(input('Use secure connection? (1-yes, 0-no): '))
        factory = HTTPFactory(is_secure)
    elif protocol == 1:
        is_secure = False
        factory = FTPFactory(is_secure)
    else:
        print 'Sorry, wrong answer'

    connector = Connector(factory)
    try:
        content = connector.read(domain, path)
    except urllib2.URLError, e:
        print 'Cannot access the resources with this method'
    else:
        print connector.parse(content) #calls the __call__ of parse attribute which is parser

