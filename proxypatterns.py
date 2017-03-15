from abc import ABCMeta, abstractmethod
import random

class AbstractSubject(object):
    """A common interface for the real and proxy objects"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, reverse=False):
        pass


class RealSubject(AbstractSubject):
    def __init__(self):
        self.digits = []

        for i in xrange(100000):
            self.digits.append(random.random())

    def sort(self, reverse=False):
        self.digits.sort()

        if reverse:
            self.digits.reverse()

"""A proxy class will be instatiated by the client code- which contains
the count of references to the RealSubject and keeps the only instance of
RealSubject creating only if it has not been created before.
In case it has been created, the reference counter is incremented!"""
class Proxy(AbstractSubject):
    reference_count = 0
    def __init__(self):
        """A constructor which creates an object if it is not exist and caches
        it otherwise"""
        if not getattr(self.__class__, 'cached_object', None):
            self.__class__.cached_object = RealSubject()
            print 'Created new object'
        else:
            print 'Using the cached object'
        self.__class__.reference_count += 1
        print 'Count of references = ', self.__class__.reference_count

    def sort(self, reverse=False):
        """The args are logged by the proxy"""
        print 'Called sort method with args: '
        print locals().items()
        self.__class__.cached_object.sort(reverse=reverse)

    def __del__(self):
        """Decreases the reference"""
        self.__class__.reference_count -= 1
        if self.__class__.reference_count == 0:
            print 'Number of reference_count is 0. Deleting the cached object..'
            del self.__class__.cached_object
        print 'Deleted object. Count of objects = ', self.__class__.reference_count


#client code
if __name__ == '__main__':
    proxy1 = Proxy()
    print
    proxy2 = Proxy()
    print
    proxy3 = Proxy()
    print
    proxy1.sort(reverse=True)
    print
    print 'Deleting proxy2'
    del proxy2
    print
    print 'the other objects are deleted upon program temrination'

