#!/usr/bin/python
# encoding: utf-8

import blynklib
import blynktimer

#===================================#
# Display Constants                 #
#===================================#
BRICK_TO_VPIN   = {
	0: 2,
	1: 3,
	2: 4,
	3: 5,
	4: 6,
	5: 7,
	6: 8,
}
VPIN_TO_BRICK   = {
	2: 0,
	3: 1,
	4: 2,
	5: 3,
	6: 4,
	7: 5,
	8: 6,
}
BATT_VPIN       = 1
BATT_WARNING_P  = 20.0 # 20%
CELL_WARNING_V  = 3.25 # 20%
BATT_COLOR_HIGH = '#00FF00'
BATT_COLOR_LOW  = '#FF0000'
JOYSTICK_VPIN   = 0   # set to MERGE
#===================================#
# Battery/Cell Constants            #
#===================================#
CELL_MIN_V      = 3.0  # 0%
CELL_MAX_V      = 4.2  # 100%

#===================================#
# Motor Constants                   #
#===================================#
MOTOR_CURRENT_SPEED   = 0
MOTOR_SPEED_STEP_NUM  = 5   # large instantaneous increases in motor speed 
						    # will be divided up into smaller chunks for 
						    # smoother controller experience
MOTOR_SPEED_STEP_TIME = 100 # ms
#===================================#
# Blynk Setup                       #
#===================================#
BLYNK_AUTH = 'j4ZPgxb0Z6rSJ0T7nI_Hj6CAjgr-fb9X'

# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)
# create timers dispatcher instance
timer = blynktimer.Timer()
#===================================#

# advanced options of lib init
# from __future__ import print_function
# blynk = blynklib.Blynk(BLYNK_AUTH, server='blynk-cloud.com', port=80, ssl_cert=None,
#                        heartbeat=10, rcv_buffer=1024, log=print)

# register handler for Virtual Pin V0 writing by Blynk App.
# when a widget in Blynk App sends Virtual Pin data to server within given configurable interval (1,2,5,10 sec etc) 
# server automatically sends notification about write virtual pin event to hardware
# this notification captured by current handler 
@blynk.handle_event('write V{}'.format(JOYSTICK_VPIN))
def joystick_write_handler(pin, value):
    '''
    write joystick val to motor
    '''
    x_val, y_val = value

    print('Joystick x_val: {}'.format(x_val))
    print('Joystick y_val: {}'.format(y_val))


@timer.register(pin=BATT_VPIN, interval=5, run_once=False)
def write_to_virtual_pin(pin):
    '''
    update total battery %
    '''
    battery_percent = '<YourSensorData>'

    print('writing {} to vpin {}'.format(battery_percent, pin))
    blynk.virtual_write(pin, battery_percent)

    if battery_percent < BATT_WARNING_P:
		# set red color for the widget UI element
		blynk.set_property(pin, 'color', BATT_COLOR_LOW)


@timer.register(pin=BRICK_TO_VPIN[0], interval=5, run_once=False)
@timer.register(pin=BRICK_TO_VPIN[1], interval=5, run_once=False)
@timer.register(pin=BRICK_TO_VPIN[2], interval=5, run_once=False)
@timer.register(pin=BRICK_TO_VPIN[3], interval=5, run_once=False)
@timer.register(pin=BRICK_TO_VPIN[4], interval=5, run_once=False)
@timer.register(pin=BRICK_TO_VPIN[5], interval=5, run_once=False)
@timer.register(pin=BRICK_TO_VPIN[6], interval=5, run_once=False)
def write_to_virtual_pin(pin):
    '''
    update all cell_v's
    '''
    cell_v = '<YourSensorData>'

    print('writing {} to vpin {}'.format(cell_v, pin))
    blynk.virtual_write(pin, cell_v)

    if cell_v <= CELL_WARNING_V:
		# set red color for the widget UI element
		blynk.set_property(pin, 'color', BATT_COLOR_LOW)

# main loop that starts program and handles registered events
while True:
    blynk.run()
    timer.run()