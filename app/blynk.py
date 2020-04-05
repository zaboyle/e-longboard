#!/usr/bin/python
# encoding: utf-8

import os
import blynklib
import blynktimer
import utils
import yaml

# Setup
#======================================================================#
# load config parameters. select default configuration
CONFIG = 'default'
params = yaml.load(file(os.path.join('app/config.yml'), 'r'))
params = params[CONFIG]['blynk']

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
def write_to_virtual_pin(vpin):
    '''
    update total battery %
    '''
    battery_percent = 25 # '<YourSensorData>'

    print('writing {} to vpin {}'.format(battery_percent, vpin))
    blynk.virtual_write(vpin, battery_percent)

	# set color for the widget UI element accordingly
    if battery_percent < params['BATT_WARNING_P']:
        blynk.set_property(vpin, 'color', params['BATT_COLOR_LOW'])
    else:
        blynk.set_property(vpin, 'color', params['BATT_COLOR_HIGH'])


@timer.register(pin=params['vpins']['BRICK_TO_VPIN'][0], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(pin=params['vpins']['BRICK_TO_VPIN'][1], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(pin=params['vpins']['BRICK_TO_VPIN'][2], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(pin=params['vpins']['BRICK_TO_VPIN'][3], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(pin=params['vpins']['BRICK_TO_VPIN'][4], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(pin=params['vpins']['BRICK_TO_VPIN'][5], interval=params['REFRESH_INTERVAL'], run_once=False)
@timer.register(pin=params['vpins']['BRICK_TO_VPIN'][6], interval=params['REFRESH_INTERVAL'], run_once=False)
def write_to_virtual_pin(pin):
    '''
    update all cell_v's
    '''
    cell_v = 3.69987 # '<YourSensorData>'

    print('writing {} to vpin {}'.format(cell_v, pin))
    blynk.virtual_write(pin, cell_v)

	# set color for the widget UI element accordingly
    if cell_v <= params['CELL_WARNING_V']:
	    blynk.set_property(pin, 'color', params['BATT_COLOR_LOW'])
    else:
        blynk.set_property(pin, 'color', params['BATT_COLOR_HIGH'])

# main loop that starts program and handles registered events
if __name__ == '__main__':
    while True:
        blynk.run()
        timer.run()
