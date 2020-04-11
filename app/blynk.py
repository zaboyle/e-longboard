#!/usr/bin/python
# encoding: utf-8

import os
import socket
import threading
import argparse
import json
import yaml
from time import sleep
import blynklib
import blynktimer
import utils

# Setup
#======================================================================#
parser = argparse.ArgumentParser(description='e-longboard BMS Blynk interaction script')
parser.add_argument('-c', '--config', type=str, default='default', help='specific configuration specified in config.yml')
parser.add_argument('-f', '--config_file', type=argparse.FileType(mode='r'), required=True, help='location of config file')
parser.add_argument('-p', '--alert_port', type=int, default=4000, help='port to listen on for alerts')

args, other_args = parser.parse_known_args()
# load config parameters. select default configuration
params = yaml.load(args.config_file)
params = params[args.config]['blynk']

# moved token to environment var
BLYNK_AUTH = os.environ.get('BLYNK_AUTH')
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)
# create timers dispatcher instance
timer = blynktimer.Timer()
#======================================================================#

# advanced options of lib init
# from __future__ import print_function
# blynk = blynklib.Blynk(
#   BLYNK_AUTH,
#   server='blynk-cloud.com',
#   port=80, ssl_cert=None,
#   heartbeat=10,
#   rcv_buffer=1024,
#   log=print
# )

# FIXME
@blynk.handle_event('internal_acon')
def app_connect_handler(*args):
    print('app connected!!')

@blynk.handle_event('internal_adis')
def app_disconnect_handler(*args):
    print('app disconnected!!')

# register handler for Virtual Pin V0 writing by Blynk App.
# when a widget in Blynk App sends Virtual Pin data to server within given configurable interval (1,2,5,10 sec etc) 
# server automatically sends notification about write virtual pin event to hardware
# this notification captured by current handler 
@blynk.handle_event('write V{}'.format(params['vpins']['JOYSTICK']))
def joystick_write_handler(vpin, value):
    '''
    write joystick val to motor
    '''
    x_val, y_val = value

    print('Joystick x_val: {}'.format(x_val))
    print('Joystick y_val: {}'.format(y_val))

@timer.register(vpin=params['vpins']['BATT_LARGE'], interval=params['REFRESH_INTERVAL'], run_once=False)
def write_to_virtual_pin_batt(vpin):
    '''update total battery %'''
    battery_percent = 25 # '<YourSensorData>'

    print('writing {} to vpin {}'.format(battery_percent, vpin))
    blynk.virtual_write(vpin, battery_percent)

	# set color for the widget UI element accordingly
    if battery_percent < params['BATT_WARNING_P']:
        blynk.set_property(vpin, 'color', params['BATT_COLOR_LOW'])
    else:
        blynk.set_property(vpin, 'color', params['BATT_COLOR_HIGH'])

@timer.register(vpin=params['vpins']['BRICK_TO_VPIN_VOLT'][0], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(vpin=params['vpins']['BRICK_TO_VPIN_VOLT'][1], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(vpin=params['vpins']['BRICK_TO_VPIN_VOLT'][2], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(vpin=params['vpins']['BRICK_TO_VPIN_VOLT'][3], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(vpin=params['vpins']['BRICK_TO_VPIN_VOLT'][4], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(vpin=params['vpins']['BRICK_TO_VPIN_VOLT'][5], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(vpin=params['vpins']['BRICK_TO_VPIN_VOLT'][6], interval=params['REFRESH_INTERVAL'], run_once=False)
def write_to_virtual_pin_cell(vpin):
    '''update all cell_v's'''
    cell_v = 3.69987 # '<YourSensorData>'

    print('writing {} to vpin {}'.format(cell_v, vpin))
    blynk.virtual_write(vpin, cell_v)

	# set color for the widget UI element accordingly
    if cell_v <= params['CELL_WARNING_V']:
	    blynk.set_property(vpin, 'color', params['BATT_COLOR_LOW'])
    else:
        blynk.set_property(vpin, 'color', params['BATT_COLOR_HIGH'])

class Program:

    def __init__(self):
        # use to terminate threads on keyboardinterrupt
        self.exit_request = False

    def alert_listener(self):
        '''listen for alerts from the bms script'''

        # Create an INET, STREAMing socket, this is TCP
        # TCP = socket.SOCK_STREAM
        # UDP = socket.SOCK_DGRAM
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the server
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', args.alert_port))
        sock.listen(5)
        # Socket accept() and recv() will block for a maximum of 1 second. If 
        # you omit this, it blocks indefinitely, waiting for a connection.
        # keep here in order to stop program on ctrl + C
        sock.settimeout(1)

        while not self.exit_request:
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

    def blynk_main(self):
        while not self.exit_request:
            blynk.run()
            timer.run()

    def run(self):
        try:
            blynk_thread = threading.Thread(target=self.blynk_main)
            alert_thread = threading.Thread(target=self.alert_listener)
            blynk_thread.start()
            alert_thread.start()
            print('blynk script running...')
            # keep this main loop running to catch any
            # keyboardinteerrupts, then send a request to finish thread execution
            while True:
                sleep(1)

        except KeyboardInterrupt:
            self.exit_request = True
            print('\nblynk script requesting to exit...')
            blynk_thread.join()
            alert_thread.join()
            print('blynk script terminated')

if __name__ == '__main__':
    p = Program()
    p.run()