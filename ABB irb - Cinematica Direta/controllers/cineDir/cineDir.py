# -*- coding: utf-8 -*-

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

import tkinter as tk
import tempfile
from ikpy.chain import Chain
from controller import Supervisor

print("\x1b[2J\x1b[1;1H")


class Robot:
    def __init__(self):
        self.supervisor = Supervisor()
        self.timeStep = int(4 * self.supervisor.getBasicTimeStep())
        # Create the arm chain from the URDF
        with tempfile.NamedTemporaryFile(suffix='.urdf', delete=False) as file:
            filename = file.name
            file.write(self.supervisor.getUrdf().encode('utf-8'))
        armChain = Chain.from_urdf_file(filename)
        armChain.active_links_mask[0] = False
        # Initialize the arm motors and encoders.
        self.motors = []
        for link in armChain.links:
            if 'motor' in link.name:
                motor = self.supervisor.getDevice(link.name)
                motor.setVelocity(1.0)
                position_sensor = motor.getPositionSensor()
                position_sensor.enable(self.timeStep)
                self.motors.append(motor)
        self.arm = self.supervisor.getSelf()
        self.positions = [0 for _ in self.motors]

    def update(self):
        for motor, position in zip(self.motors, self.positions):
            motor.setPosition(position*0.01745277777)

    def simulate(self):
        self.supervisor.step(self.timeStep)


class Window:
    def __init__(self, robot):
        self.robot = robot
        self.root = tk.Tk()
        self.root.title('Posição das Juntas')
        self.root.geometry("1200x300")
        options = {
            'from_': -180,
            'to': 180,
            'length': 1200,
            'orient': tk.HORIZONTAL,
            'command': self.update_robot_positions
        }
        self.sliders = [tk.Scale(self.root, **options) for _ in range(0, 7)]
        [slider.pack() for slider in self.sliders]

    def get_sliders(self):
        return [slider.get() for slider in self.sliders]

    def update_robot_positions(self, _=None):
        *self.robot.positions, _ = self.get_sliders()
        self.robot.update()

    def run(self):
        def __run_always():
            self.robot.simulate()
            self.root.after(1, __run_always)
        __run_always()
        self.root.mainloop()


robot = Robot()
window = Window(robot)
window.run()
