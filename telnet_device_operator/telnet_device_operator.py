import telnetlib
import json

class IOSTelnetOperator():
	def __init__(self, host, username, password, port='23'):
		self.hostname = host
		self.username = username
		self.password = password
		self.port = port

	def connect(self):
		self.connection = telnetlib.Telnet(self.hostname)
		self.connection.read_until(b"Username: ")
		self.connection.write(bytes((self.username+'\n').encode('ascii')))
		self.connection.read_until(b"Password: ")
		self.connection.write(bytes((self.password+'\n').encode('ascii')))
		self.device_name = self.connection.read_until(b"#")
		self.device_name = bytes(self.device_name.decode('ascii').split('\r\n')[-1], 'ascii')
		self.connection.write(bytes(('terminal length 0'+'\n').encode('ascii')))
		self.connection.read_until(self.device_name)

	def close(self):
		self.connection.close()

	# def config_operation(self, operation, proc_func):
	# 	self.connection.write(bytes((operation+'\n\n').encode('ascii')))
	# 	# output = self.connection.read_until(self.device_name+bytes('(config)','ascii'))
	# 	output = self.connection.read_some()
	# 	output = self.connection.read_some()
	# 	return proc_func(output)	

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
	ITO = IOSTelnetOperator('ipv4', 'username', 'password')
	ITO.connect()
	output = ITO.show_operation('show running-config')
	# output = ITH.config_operation('config', test_func)

	print(output)
	print(ITO.get_device_name())

if __name__ == '__main__':
	main()