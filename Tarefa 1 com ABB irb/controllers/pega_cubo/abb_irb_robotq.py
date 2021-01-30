print("\x1b[2J\x1b[1;1H")
from controller import Supervisor

supervisor = Supervisor()
timeStep = int(4 * supervisor.getBasicTimeStep())

motors = []
fingers = []
for index in range(0, supervisor.getNumberOfDevices()):
    device = supervisor.getDeviceByIndex(index)
    print(device.getName())
    name = device.getName()
    if 'sensor' in name:
        continue
    elif 'motor' in name:
        device.setVelocity(1.0)
        position_sensor = device.getPositionSensor()
        position_sensor.enable(timeStep)
        motors.append(device)
    elif 'finger' in name:
        device.setVelocity(1.0)
        position_sensor = device.getPositionSensor()
        position_sensor.enable(timeStep)
        fingers.append(device)

print(f'motors  ({len(motors )}): {[motor.getName()  for motor  in motors]}')
print(f'fingers ({len(fingers)}): {[finger.getName() for finger in fingers]}')


def moveTo(positions):
    for motor, position in zip(motors, positions):
        motor.setPosition(position * 0.01745277777)


def garra(positions):
    #positions = [
        #sorted([positions[0],   3, 70])[0],
        #sorted([positions[1],   0, 90])[1],
        #sorted([positions[2], -70, -3])[2],
    #]

    fingers[1].setPosition(positions[0] * 0.01745277777)
    fingers[2].setPosition(positions[1] * 0.01745277777)
    fingers[3].setPosition(positions[2] * 0.01745277777)

    fingers[5].setPosition(positions[0] * 0.01745277777)
    fingers[6].setPosition(positions[1] * 0.01745277777)
    fingers[7].setPosition(positions[2] * 0.01745277777)

    fingers[8].setPosition(positions[0] * 0.01745277777)
    fingers[9].setPosition(positions[1] * 0.01745277777)
    fingers[10].setPosition(positions[2] * 0.01745277777)
