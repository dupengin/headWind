"""
Author: Pearce Duffy 
Revision: 002 
Reviewers: None
-----------------------------------------------------------------------------------------------------------------------------------------
The programme takes a gpx file and works out the relative wind speed and head winds faced based on the path of the GPX file. 
This was developed with cycling in mind but can be used for other activites, e.g. running.
Weather data is taken from a third party website using an API. https://www.visualcrossing.com/weather-data. 
API data requests are capped at 1000 records a day. Therefore the programme allows for test data to be used in place of an API request

This is just a test project to see what can be done, it is not intended for commercial projects. 

Other sources: Research has shown that there is an exisitng website that does this https://mywindsock.com/. 
The programme below was developed without reviewing the windsock site or methodologies. 

The output will be a map displaying the GPX route using a poly line which will be colored depending on the headwind.
As it is likley the same route will be used on the return journey, i.e it will start and finish at the same point, 
direcitonal arrows will be added to the poly line.

This programme is just for wind speed not drag. - this could be added at a later date using some very rough assumptions on the drag coefficient and cross sectional area. 

-------------------------------------------------------------------------------------------------------------------------------------------

Below is the main programme calling sub-programmes and launching flask application to dispaly results
"""



#import of various libaries and functions 
from flask import Flask, render_template
import folium
import branca.colormap as cm
from folium import plugins


import matplotlib.pyplot as plot
import io
import base64
import os

#import of functions created for this project
from windSpeedRequest import requestWeatherData
from relWindSpeed import relWindSpeed
from saveData import saveDataCSV
from speedDirectionCalc import speedDirectionCalculator
from movingPointAve import movingPointAve


 
app = Flask(__name__)

# 
@app.route('/')
def index():
    
    headWind, ex_data = get_data()  #call to t

    # Generate map
    map_heatmap = generate_line(ex_data, headWind)

    #graph = generate_graph(headWind, ex_data)

    # Render the map in HTML template
    return render_template('heatmap.html', map_heatmap=map_heatmap._repr_html_())


def get_data():
    testMode = False #Select True or False for test mode. When set to false it will make API requets

    #GPX filename explicitly declared for this funciton. Future version will include GUI input for filename
    print(os.getcwd())
    usrBearing, usrSpeed, ex_data = speedDirectionCalculator('2023-07-05_1198576652_Cycling.gpx')  

    windSpeeds, windDirs = requestWeatherData(ex_data, testMode)
    headWind = relWindSpeed(usrSpeed, usrBearing, windSpeeds, windDirs)
    ex_data, headWind = movingPointAve(ex_data, headWind) 

    #filename of saved data is set within the funciton. Future rev to allow for user set output file name
    saveDataCSV(ex_data, headWind, usrBearing, usrSpeed) 
    
    return(headWind, ex_data)


def generate_line(ex_data, headWind):
    #centre point will be set to the coords in the middle of the data array
    lat_c = ex_data[int(len(ex_data)/2)]["lat"]
    lon_c = ex_data[int(len(ex_data)/2)]["longit"]
    

    #Create a folium map centered on the mid coords in the middle of the data array
    map_line = folium.Map(location=[lat_c, lon_c], zoom_start=10)

    # Create a colormap for the line color based on head wind variable
    colormap = cm.LinearColormap(colors=['blue','white', 'red'], vmin=min(headWind),vmax=max(headWind))
    
    #Arrays declared for creating the poly line below
    coord=[]
    color = []

    # create an array of coords for the poly line
    for i in range (int(len(ex_data)-1)):
        t = (ex_data[i]["lat"], ex_data[i]["longit"])
        coord.append(t)

    #Create the poly line with the appropoate coloring and arrows for direction      
    for i in range(len(coord)-1):
        seg_coord = coord[i:i+2]
        color = colormap(headWind[i])
        polyline = folium.PolyLine(locations = seg_coord,color = color, weight = 3)
        wind_textpath = plugins.PolyLineTextPath(
        polyline, "                 >                   ", repeat=True, offset=7, attributes={"fill": "#000000", "font-weight": "bold", "font-size": "24"})
        map_line.add_child(polyline)
        map_line.add_child(wind_textpath)

    
        
    



    # Add the colormap to the map
    colormap.caption = 'HeadWind'
    colormap.add_to(map_line)

    
    return map_line



#funciton to create line graph, not used just yet 

def generate_graph( headWind, ex_data):

    timeSecs = [] #create an array for the x axis data set


    #for loop to generate the data set of seconds
    for i in range (len(ex_data)-1):
        t = ex_data[i]['time']
        hours, mins, secs = t.split(":")
        tSecs = (hours * 3600) + (mins * 60) + secs
        timeSecs.append(tSecs)
    
    #declaring the x and y axis data sets
    x = headWind
    y = timeSecs

    #plotting the graph
    plot.scatter(x , y)
    plot.xlabel ('X')
    plot.ylabel ('Y')
    plot.title('Head Wind Graph')


    #commands to convert plot into an image for web-page render
    img = io.BytesIO()
    plot.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    #return the graph to the main programme for rendering
    return (plot_url)
    
    



if __name__ == '__main__': #cmd to run programme and it is run directly from this pager
    app.run(debug=True)