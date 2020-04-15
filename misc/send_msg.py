import socket
import json
import datetime

ADDRESS = 'localhost'
PORT = 4000

# create socket with TCP, IPV4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
sock.connect((ADDRESS, PORT))

data = {
	'alert_name': 'CELL_BLEED',
	'timestamp': str(datetime.datetime.now())
}
message_str = json.dumps(data).encode('utf-8')

print('sending data {}'.format(message_str))
# send a message
sock.sendall(message_str)
sock.close()