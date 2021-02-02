import abb_irb_robotq as abb

while abb.supervisor.step(abb.timeStep) != -1:
    
    time = abb.supervisor.getTime()
    
    if time < 2:
        abb.moveTo([0, 0, 0, 0, 0, 0])
        
    elif time < 4:
        abb.garra([360, 360, 360])
        
    elif time < 6:
        abb.moveTo([-45, 30, 30, 0, 0, 0])
        
    elif time < 8:
        abb.garra([0, 0, 0])

    elif time < 10:
        abb.moveTo([0, 0, 0, 0, 0, 0])