"""The functions below write set data to csv files"""

import time 

#Creation of a function to write data to csv\
#inputs = the file name, the headers of eaxh column in the csv and the data (lists) to be written to the csv, this can include multiple lists
#outputs = saved file to local directory
def write_lists_to_csv(filename, headers, *lists):
    import csv
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in zip(*lists):
            writer.writerow(row) 

#Creation of function to save the data calculated in other functions as a csv, uses the CSV writer defined above
#Input = data extracted from csv and the data calcualted in other funcitons
#Output = A csv with the calculated data saved to local directory

def saveDataCSV(ex_data, headWind, usrDir, usrSpeed ):
    longitude = []
    latitude = []
    for i in range(len(ex_data)-1):
        longitude.append(ex_data[i]['longit'])
        latitude.append(ex_data[i]['lat'])
    timestr = time.strftime("%Y%m%d-%H%M%S") #creation of string to use in the filename, it uses the time and date of when this funciton was called
    filename = 'output' + timestr + ".csv" 
    headers = ['longitude', 'latitude', 'Head Wind', 'User Direction', 'User Speed', 'Resultant Wind Speed', 'Resultant Wind Direction']

    write_lists_to_csv(filename, headers, longitude, latitude, headWind, usrDir, usrSpeed) #call the CSV writer, including the data sets to be written

#Function used to write test data that can be used in place of an API call.
#Input = Data taken from a previous API call and limited to only the data the programme requires i.e. wind speed and direciton
#Output = a CSV written to the local directory

def saveTestDataCSV(windSpeed, WindDir ):
    
    
    filename = 'test_data_0.csv'
    headers = ['Wind Speed', 'Wind Direction']

    write_lists_to_csv(filename, headers, windSpeed, WindDir) #call the CSV writer, including the data sets to be written