#!/usr/bin/env pybricks-micropython

# Ricardo Controller EV3
# Copyright (C) 2025 Jose H
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

# Configuration
DRIVE_SPEED = 400  # degrees/second
TURN_RATE = 150    # degrees/second
ARM_SPEED = 100    # degrees/second
is_driving = False

# Commands
STOP_COMMAND_DRIVE = "STOP_DRIVE"
STOP_COMMAND_ARM = "STOP_ARM"
STOP_COMMAND_ALL = "STOP_ALL"
FORWARD_COMMAND = "FORWARD"
BACKWARD_COMMAND = "BACKWARD"
LEFT_COMMAND = "LEFT"
RIGHT_COMMAND = "RIGHT"
ARM_UP_COMMAND = "ARM_UP"
ARM_DOWN_COMMAND = "ARM_DOWN"


# Objects 
ev3 = EV3Brick()
ev3.speaker.set_speech_options(language='es-la', voice='m1') # 🇲🇽

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
arm_motor = Motor(Port.D) 

# Bluetooth
server = BluetoothMailboxServer()
mbox = TextMailbox('control', server)
print("Robot Waiting for Connection...")
ev3.speaker.beep()
server.wait_for_connection()
print("Connected!")
ev3.speaker.beep(frequency=500, duration=200)
ev3.speaker.say("Connectado! Hola Regina")

# Main
while True:
    received_command = mbox.read()

    if received_command:
        print("Received:", received_command)

        # Motor Control
        if received_command == FORWARD_COMMAND:
            arm_motor.stop() # Stop arm if it was moving
            is_driving = True
            left_motor.run(DRIVE_SPEED)
            right_motor.run(DRIVE_SPEED)
        elif received_command == BACKWARD_COMMAND:
            arm_motor.stop() # Stop arm if it was moving
            is_driving = True
            left_motor.run(-DRIVE_SPEED)
            right_motor.run(-DRIVE_SPEED)
        elif received_command == LEFT_COMMAND:
            arm_motor.stop() # Stop arm if it was moving
            is_driving = True
            left_motor.run(-TURN_RATE)
            right_motor.run(TURN_RATE)
        elif received_command == RIGHT_COMMAND:
            arm_motor.stop() # Stop arm if it was moving
            is_driving = True
            left_motor.run(TURN_RATE)
            right_motor.run(-TURN_RATE)
        # Add a STOP command handling
        elif received_command == STOP_COMMAND_DRIVE:
             left_motor.stop()
             right_motor.stop()
             is_driving = False
        # Arm Motor Control
        elif received_command == ARM_UP_COMMAND:
            if not is_driving: # Only move arm if not driving
                arm_motor.run(ARM_SPEED)
            else:
                print("Cannot move arm while driving.")
        elif received_command == ARM_DOWN_COMMAND: 
            if not is_driving: # Only move arm if not driving
                arm_motor.run(-ARM_SPEED)
            else:
                print("Cannot move arm while driving.")
        elif received_command == STOP_COMMAND_ARM:
             arm_motor.stop()

        #Stop All
        elif received_command == STOP_COMMAND_ALL: 
             left_motor.stop()
             right_motor.stop()
             arm_motor.stop()
             is_driving = False
    else:

        pass

    # Small delay
    wait(10)
