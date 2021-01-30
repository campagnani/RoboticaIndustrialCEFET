import abb_irb_robotq as abb

while abb.supervisor.step(abb.timeStep) != -1:
    
    time = abb.supervisor.getTime()
    
    if time > 2:
        abb.moveTo([0, 0, 0, 0, 0, 0])
        abb.garra([360, 360, 360])

    if time > 4:
        abb.moveTo([-45, 30, 30, 0, 0, 0])
        abb.garra([0, 0, 0])
