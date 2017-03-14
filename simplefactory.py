class SimpleFactory(object):
    @staticmethod
    def build_connection(protocol):
        if protocol == 'http':
            return HTTPConnection()
        elif protocol == 'ftp':
            return FTPConnection()
        else:
            raise RuntimeError('Unknown Protocol')

if __name__ == '__main__':
    protocol = raw_input('Which protocol to use? (http or ftp): ')
    protocol = SimpleFactory.build_connection(protocol)
    protocol.connect()
    print protocol.get_response()
