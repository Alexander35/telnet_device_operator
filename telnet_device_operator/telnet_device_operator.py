import telnetlib
import json
from socket import gaierror

class IOSTelnetOperator():
    def __init__(self, host, username, password, port='23'):
        self.hostname = host
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        try:
            self.connection = telnetlib.Telnet(self.hostname, self.port, 20)
            self.connection.expect([b"Username: "], 5)
            self.connection.write(bytes((self.username+'\n').encode('ascii')))
            self.connection.expect([b"Password: "], 5)
            self.connection.write(bytes((self.password+'\n').encode('ascii')))

            (status, _, self.device_name) = self.connection.expect([b".+#"], 5)
            if status != 0:
                return {'unexpected_error': self.device_name.decode('ascii')}

            self.device_name = bytes(self.device_name.decode('ascii').split('\r\n')[-1], 'ascii')
            self.connection.write(bytes(('terminal length 0'+'\n').encode('ascii')))
            self.connection.read_until(self.device_name)
        except gaierror as exc:
            return {'hostname_error': '{}'.format(exc)}
        except TimeoutError as exc:
            return {'timeout_error': '{}'.format(exc)}
        except EOFError as exc:
            return {'eof_error': '{}'.format(exc)}
        except Exception as exc:
            return {'other_exception': '{}'.format(exc)}

    def close(self):
        self.connection.close()

    # def config_operation(self, operation, proc_func):
    #   self.connection.write(bytes((operation+'\n\n').encode('ascii')))
    #   # output = self.connection.read_until(self.device_name+bytes('(config)','ascii'))
    #   output = self.connection.read_some()
    #   output = self.connection.read_some()
    #   return proc_func(output)

    # show etc ...
    def show_operation(self, operation):
        self.connection.write(bytes((operation+'\n').encode('ascii')))
        output = self.connection.read_until(self.device_name)
        return output

    def get_device_name(self):
        return self.device_name


def test_func(raw_data):
    print(raw_data)

def main():
    ITO = IOSTelnetOperator('10.11.0.1', 'everiste', 'wert')
    status = ITO.connect()
    if status is not None:
        print(status)
        exit(1)
    output = ITO.show_operation('show running-config')
    # output = ITH.config_operation('config', test_func)

    print(output)
    print(ITO.get_device_name())

if __name__ == '__main__':
    main()
