# telnet_device_operator

It can get output from the simple show commands like sh run, sh int... or something else


```
def main():
	ITO = IOSTelnetOperator('ipv4', 'username', 'password')
	ITO.connect()
	output = ITO.show_operation('show running-config')

	print(output)
	print(ITO.get_device_name())
```	