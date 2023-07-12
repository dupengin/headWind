def movingPointAve(ex_data, headWind):
    """Code to reduce the noise in the results and highlight the underlying trends
        The Simple Moving Average method has been selected for this as it is suitable ot be used with time series data, equation:
        
                 
                      _n_       
                     \     
               1      \    P
        SMA  = -      /     i
           k   k     /___
                  i = n - k + 1

        
        
        """
    

    #The data will be averaged over a 30 sec timestep, as the data is recorded in 1 sec intervals this means k = 30
    k = 30 
    new_headWind = [] #new array for storing the SMA data

    #for loop to create the SMA data
    for i in range (0, len(headWind), k):
        x = i + k
        s = sum(headWind[i:x])
        ave = s / k
        new_headWind.append(ave)
    
    new_ex_data = [] #new array to store the reduced number of data points

    #for loop to extract the ex_data values at the mid point of the averaged wind speed data
    for i in range(int(k/2)-1, len(ex_data) - (int(k/2)-1), k):
        new_ex_data.append(ex_data[i])
    
    return (new_ex_data, new_headWind)  