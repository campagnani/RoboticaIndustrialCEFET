# Copyright 1996-2021 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Demonstration of inverse kinematics using the "ikpy" Python module."""
print("\x1b[2J\x1b[1;1H")
import threading
import tkinter as tk
import sys
import tempfile
import os

try:
    import ikpy
    from ikpy.chain import Chain
except ImportError:
    sys.exit('The "ikpy" Python module is not installed. '
             'To run this sample, please upgrade "pip" and install ikpy with this command: "pip install ikpy"')

import math
from controller import Supervisor

if ikpy.__version__[0] < '3':
    sys.exit('The "ikpy" Python module version is too old. '
             'Please upgrade "ikpy" Python module to version "3.0" or newer with this command: "pip install --upgrade ikpy"')


IKPY_MAX_ITERATIONS = 4

# Initialize the Webots Supervisor.
supervisor = Supervisor()
timeStep = int(4 * supervisor.getBasicTimeStep())

# Create the arm chain from the URDF
filename = None
with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
    filename = file.name
    file.write(supervisor.getUrdf().encode('utf-8'))
armChain = Chain.from_urdf_file(filename)
for i in [0, 6]:
    armChain.active_links_mask[0] = False

# Initialize the arm motors and encoders.
motors = []
for link in armChain.links:
    if 'motor' in link.name:
        motor = supervisor.getDevice(link.name)
        motor.setVelocity(1.0)
        position_sensor = motor.getPositionSensor()
        position_sensor.enable(timeStep)
        motors.append(motor)

# Get the arm and target nodes.
arm = supervisor.getSelf()
posiçãoAngular = [0,0,0,0,0,0]

#interface Grafica
def interfaceGrafica():
    root = tk.Tk()
    root.title('Controlar juntas do robô e garra com sliders')
    root.geometry("800x600")
    
    def update():
        for i in range(0,6):
            posiçãoAngular[i] = slide[i].get()
        garra = slide[6].get()
    
    slide = [0,0,0,0,0,0,0]
    
    for i in range(0,7):
        slide[i] = tk.Scale(root, from_=-180, to=180, length=800, orient=tk.HORIZONTAL)#,command = update)
        slide[i].pack()
    
    go = tk.Button(root, text="Move!", command = update).pack()
    
    root.mainloop()


class ThreadDoThalles(threading.Thread):
    def __init__(self):
         super(ThreadDoThalles, self).__init__()

    def run(self):
        interfaceGrafica()

thread1 = ThreadDoThalles()
thread1.start()

    
while supervisor.step(timeStep) != -1:
    for i in range(len(motors)):
        motors[i].setPosition(posiçãoAngular[i]*0.01745277777)
    pass
    