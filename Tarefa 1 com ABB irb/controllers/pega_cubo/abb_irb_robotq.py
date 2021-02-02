print("\x1b[2J\x1b[1;1H")
from controller import Supervisor

supervisor = Supervisor()
timeStep = int(4 * supervisor.getBasicTimeStep())

motors = []
fingers = []
for index in range(0, supervisor.getNumberOfDevices()):
    device = supervisor.getDeviceByIndex(index)
    #print(device.getName())
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

#print(f'motors  ({len(motors )}): {[motor.getName()  for motor  in motors]}')
#print(f'fingers ({len(fingers)}): {[finger.getName() for finger in fingers]}')

rad = 0.01745329251
def moveTo(positions):
    for motor, position in zip(motors, positions):
        motor.setPosition(position * rad)


def garra(positions):
    positions = [
        sorted([positions[0],   3, 69])[1],
        sorted([positions[1],   0, 90])[1],
        sorted([positions[2],   3, 69])[1]
    ]
    
    fingers[1].setPosition (positions[0] *  rad)
    fingers[2].setPosition (positions[1] *  rad)
    fingers[3].setPosition (positions[2] * -rad)

    fingers[5].setPosition (positions[0] *  rad)
    fingers[6].setPosition (positions[1] *  rad)
    fingers[7].setPosition (positions[2] * -rad)

    fingers[8].setPosition (positions[0] *  rad)
    fingers[9].setPosition (positions[1] *  rad)
    fingers[10].setPosition(positions[2] * -rad)
