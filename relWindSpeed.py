"""
code to calculate the relative wind speed based on the direciton and speed of the user and the wind


Headwind calcualtion 
Vc + Vwx = Vh
Vwx = Vw * cos(theta - delta)
theta = wind bearing 
delta = usrBearing
"""


def relWindSpeed(usrSpeed, usrBearing, windSpeeds, windDirs):
    import math
    
    headWind = []

    for i in range(len(usrSpeed)):
        # calculate the wind users velocity components in the x & y direciton
    
        V_wx = windSpeeds[i] * math.cos(math.radians(windDirs[i] - usrBearing[i]))
        m = math.cos(windDirs[i] - usrBearing[i])
        V_h = usrSpeed[i] + V_wx
        
        

        headWind.append(V_h)
    
    return (headWind) 
    