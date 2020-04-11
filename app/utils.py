import threading
import socket
import json


def send_alert_handler(address, port, data):
	'''send data to address on port'''
	# create socket with TCP, IPV4
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# connect to the server
	sock.connect((address, port))

	message_str = json.dumps(data).encode('utf-8')

	print('sending data {}'.format(message_str))
	# send a message
	sock.sendall(message_str)
	sock.close()

def send_alert(address, port, data):
	'''send alert non-blocking'''
	handler_thread = threading.Thread(
		target=send_alert_handler,
		args=(address, port, data,)
	)
	handler_thread.start()
