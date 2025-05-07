#!/usr/bin/env pybricks-micropython

# Regina Controller EV3
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
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Button
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# Commands
COMMAND_DELAY_MS = 150 
STOP_COMMAND_DRIVE = "STOP_DRIVE"
STOP_COMMAND_ARM = "STOP_ARM"
STOP_COMMAND_ALL = "STOP_ALL" 
FORWARD_COMMAND = "FORWARD"
BACKWARD_COMMAND = "BACKWARD"
LEFT_COMMAND = "LEFT"
RIGHT_COMMAND = "RIGHT"
ARM_UP_COMMAND = "ARM_UP"
ARM_DOWN_COMMAND = "ARM_DOWN"

ev3 = EV3Brick()
ev3.speaker.set_speech_options(language='es-la', voice='f1') # 🇲🇽

# Bluetooth
client = BluetoothMailboxClient()
mbox = TextMailbox('control', client)

ev3.speaker.beep()

try:
    client.connect("Ricardo")
    wait(5000)
    ev3.speaker.say("Connectado! Hola Ricardo")
    ev3.speaker.beep(frequency=100, duration=200)
except Exception as e:
    print("failed:", e)
    wait(5000)
    exit()

# Main Control Loop
last_command_sent = None 
command_timer = StopWatch() 

while True:
    # Get the list of pressed buttons
    pressed = ev3.buttons.pressed()
    current_command = None

    # need this check lol
    if pressed is None:
        wait(50) 
        continue 

    # Check for modifier key first
    if Button.CENTER in pressed:
        # Center is held down - Arm control mode
        if Button.UP in pressed:
            current_command = ARM_UP_COMMAND
        elif Button.DOWN in pressed:
            current_command = ARM_DOWN_COMMAND
        else:
            current_command = STOP_COMMAND_ARM
    else:
        # Center is NOT held down - Driving mode
        if Button.UP in pressed:
            current_command = FORWARD_COMMAND
        elif Button.DOWN in pressed:
            current_command = BACKWARD_COMMAND
        elif Button.LEFT in pressed:
            current_command = LEFT_COMMAND
        elif Button.RIGHT in pressed:
            current_command = RIGHT_COMMAND
        else:
            # Determine what needs stopping based on the last command
            if last_command_sent in [FORWARD_COMMAND, BACKWARD_COMMAND, LEFT_COMMAND, RIGHT_COMMAND]:
                 current_command = STOP_COMMAND_DRIVE
            elif last_command_sent in [ARM_UP_COMMAND, ARM_DOWN_COMMAND]: # Check if arm was moving
                 current_command = STOP_COMMAND_ARM

    # Send if the command changed OR if it's a continuous movement command
    # And enough time has passed since the last command
    is_movement_command = current_command not in [None, STOP_COMMAND_DRIVE, STOP_COMMAND_ARM, STOP_COMMAND_ALL]

    if current_command != last_command_sent:
        print("Sending:", current_command)

        command_to_send = current_command
        if command_to_send is None:
             pass
        else:
            mbox.send(command_to_send)
            last_command_sent = current_command 
            command_timer.reset()
    elif is_movement_command and command_timer.time() > COMMAND_DELAY_MS:
        # If it's the same command, resend 
        mbox.send(current_command)
        command_timer.reset()

    wait(20)
