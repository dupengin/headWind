"""The following code calls out the weather.visualcrossing.com api service to gather weather data for the required date
The returned json packet includes weather conditions for each hour of the day, i.e each date has 24 arrays of weather data

Following information on wind data copied from the visual crossing website (https://www.visualcrossing.com/resources/documentation/weather-data/weather-data-documentation/):
*Wind speed and wind direction (wspd, wdir)*
The wind speed and wind direction indicate the wind speed for the location and time period requested. 
The hourly speed and direction values are the average (mean) of the speed and direction for the two minutes prior to the measurement being record.
Daily and other time period values display the maximum of the hourly values. 
In the Timeline Weather API, the mean and minimum daily windspeed values are also available.
The units of the data will be in miles per hour, kilometers per hour or m/s depending on the unit group.
Wind speed is typically measured 10m above ground in a location with no nearby obstructions.
The wind direction indicates the direction from where the wind is blowing from. The units of the wind direction is degrees from north. 
The value ranges from 0 degrees (from the North), to 90 degrees (from the east), 180 degrees (from the south), 270 (from the west) back to 360 degrees.


 """
def requestWeatherData(ex_data, testMode):

    import requests
    from saveData import saveTestDataCSV
    import csv

    windSpeeds = []
    windDirs = []

    #Test mode uses a pre-saved csv for wind speed and direction, this is to avoid using api requests as these are capped per day
    if (testMode):
        fileName = 'test_data_0.csv'
        print('test mode') #terminal comment to confirm that test mode is set

        with open (fileName) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                windSpeeds.append(float(row[0]))
                windDirs.append(float(row[1]))

    else:

        apiKey = 'UATQGJWXG8AYRFTJTJWEWAV4H'
        y = round(len(ex_data)/2)
        latitude = ex_data[y]['lat'] 
        longitude = ex_data[y]['longit']

        date = ex_data[y]['date']
        time = ex_data[y]['time']

        #data is recorded to the nearest hour,therefore time shall be rounded to the nearest hour
        hours, mins, secs = time.split(":")

        x = round(int(mins)/60 + int(secs)/3600)

        hoursTotal = int(hours) + x

        endpoint = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{longitude},{latitude}/{date}?key={apiKey}'

        try:
            response = requests.get(endpoint, timeout=20)
            response.raise_for_status()  # Raise an exception if the request was not successful (status code >= 400)
            dataWeather = response.json()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 429:
                print("Too Many Requests. Please try again later.") 
            else:
                print(f"HTTP Error: {response.status_code} - {err}") 
        except requests.exceptions.RequestException as err:
            print(f"An error occurred during the request: {err}")

        



        for i in range (len(ex_data) - 1):

            time = ex_data[i]['time']
            hours, mins, secs = time.split(":")

            x = round(int(mins)/60 + int(secs)/3600)

            hoursTotal = int(hours) + x

            
            windSpeeds.append( dataWeather['days'][0]['hours'][hoursTotal]['windspeed'])
            windDirs.append( (dataWeather['days'][0]['hours'][hoursTotal]['winddir']))

    #saveTestDataCSV(windSpeeds, windDirs)

    return (windSpeeds, windDirs)
    




