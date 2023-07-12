"""
Calculation of the speed and direction from the GPX file
Methodology:
- Extract gpx data using parsing code created by others - https://pypi.org/project/gpxpy/
- Calculate the direction of the user and speed based on the gpx data
    Where i is a row in the gpx data
    The direction and distance will be calcualted using the coord at i + 1
    This direction will then be the direction at time in row i
    The time difference between i + 1 and i will be used with the distance to give a resulting speed 
- store the direction and speed in a new array
- informaiton and code from following webpage was used to aid the calculation of distance and bearing between coordinates (https://github.com/TechnicalVillager/distance-bearing-calculation/blob/master/distance_bearing.py)
Assumptions:
- it is assumed that there is no acceleration between each long and latitude coordinate, they are traveling at a constant speed over this short distance

"""




#Function below extracts the required data from the GPX file, then calls another function (which is defined below) to calculate speed and bearing
def speedDirectionCalculator(fileGPX):
    import gpxpy
    import gpxpy.gpx
    
    
    #open gpx file
    gpx_file = open(fileGPX, 'r')
    gpx_data = gpxpy.parse(gpx_file) #Parsing possible due to use of https://pypi.org/project/gpxpy/

    #create 2D array to store extracted data
    global ex_data
    ex_data = []

    #for loop used to extract required data from GPX file
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                time = point.time.strftime("%H:%M:%S")
                date = point.time.strftime("%Y-%m-%d")
                longitude = point.longitude
                latitude = point.latitude

                ex_data.append({'time':time, 'date':date, 'longit':longitude, 'lat':latitude})


    bearings, speed = bearingDistance(ex_data) #bearings is in deg and speed in m/s

    return (bearings, speed, ex_data)
    
    

#funcrion below calcualtes the users speed and bearing between each data point, i.e each coordinate
#Formulas from https://github.com/TechnicalVillager/distance-bearing-calculation/blob/master/distance_bearing.py used for distance and bearings 

def bearingDistance(ex_data):
    import math
    bearings=[] #new array for storing bearing data
    dist=[] #new array for storing distance data
    diffTimes = [] #array for storing time diffence when user reaches each coordinate
    speed = [] #array for storing speed

    

    for i in range (len(ex_data)-1): 

        #each coordinate needs to be converted to radians
        lat1 = math.radians(ex_data[i]['lat'])
        lat2 = math.radians(ex_data[i+1]['lat']) 
        long1 = math.radians(ex_data[i]['longit'])
        long2 = math.radians(ex_data[i+1]['longit']) 

        
        time1 = ex_data[i]['time']
        time2 = ex_data[i+1]['time']

        diffLong = long2 - long1
        diffLat = lat2 - lat1
        
        x = math.sin(diffLong) * math.cos(lat2)
        
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        

        R = 6371e3 #Radius of earth in metres
        a = (math.sin(diffLat/2) * math.sin(diffLat/2)) + (math.cos(lat1) * math.cos(lat2) * (math.sin(diffLong/2) * math.sin(diffLong/2)))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c #distance in metres

        bearings.append(compass_bearing)
        dist.append(distance)

        hours1, mins1, secs1 = time1.split(":")
        hours2, mins2, secs2 = time2.split(":")

        seconds1 = (int(hours1) * 3600) + (int(mins1) * 60) + int(secs1)
        seconds2 = (int(hours2) * 3600) + (int(mins2) * 60) + int(secs2)
        #seconds1 = time1
        #seconds2 = time2
        diffTime = seconds2 - seconds1
        diffTimes.append(diffTime)

        if diffTime == 0 :
            diffTime = 0.1
        

       

        speed.append(distance / diffTime)

  

    return (bearings,speed) #bearings is in deg and speed is in m/s
    