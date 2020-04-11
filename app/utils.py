import threading
import socket
import json

def alert_listen(program, address, port):
	'''listen for alerts from the bms script'''

	# Create an INET, STREAMing socket, this is TCP
	# TCP = socket.SOCK_STREAM
	# UDP = socket.SOCK_DGRAM
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the server
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((address, port))
	sock.listen(5)
	# Socket accept() and recv() will block for a maximum of 1 second. If 
	# you omit this, it blocks indefinitely, waiting for a connection.
	# keep here in order to stop program on ctrl + C
	sock.settimeout(1)

	while not program.exit_request:
		# Listen for a connection for 1s.  The socket library avoids consuming
		# CPU while waiting for a connection.
		try:
			clientsocket, address = sock.accept()
		except socket.timeout:
			continue

		message_chunks = []
		while True:
			try:
				data = clientsocket.recv(4096)
			except socket.timeout:
				continue
			if not data:
				break
			message_chunks.append(data)

		clientsocket.close()

		# Decode list-of-byte-strings to UTF8 and parse JSON data
		message_bytes = b''.join(message_chunks)
		message_str = message_bytes.decode('utf-8')

		try:
			message_dict = json.loads(message_str)
		except Exception:
			print('Error: invalid alert contents')
			continue

		print('received data {}'.format(message_dict))
		yield message_dict

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
