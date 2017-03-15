"""Subject to add ,remove, and notify observers.!"""
import time

class Subject(object):
    def __init__(self):
        self.observers = []
        self.cur_time = None

    def register_observer(self, observer):
        if observer in self.observers:
            print observer, 'already in subscribed observers'
        else:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print 'No such observer in subject'

    def notify_observers(self):
        self.cur_time = time.time()
        for observer in self.observers:
            observer.notify(self.cur_time)


"""Abstract class for the observer with only one method notify which subject
used to call in its notify_observers() method"""
from abc import ABCMeta, abstractmethod
import datetime


class Observer(object):
    """Abstract class for observers providing interfaces notify() to subject"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, unix_timestamp):
        pass

"""Couple of concrete observer """
class USATimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).\
            strftime('%Y-%m-%d %I:%M:%S%p')
        print 'Observer', self.name, 'says: ', time

class EUTimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).\
            strftime('%Y-%m-%d %H:%M:%S')
        print 'Observer ', self.name, 'says: ', time



if __name__ == '__main__':
    subject = Subject()
    print 'Adding usa_time_observer'
    observer1 = USATimeObserver('USA_time_observer')
    subject.register_observer(observer1)
    subject.notify_observers()

    time.sleep(4)
    print 'Adding EU_time_observer'
    observer2 = EUTimeObserver('EU_time_observer')
    subject.register_observer(observer2)
    subject.notify_observers()

    time.sleep(2)
    print 'Removing usa_time_observer'
    subject.unregister_observer(observer1)
    subject.notify_observers()


