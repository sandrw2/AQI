#Sandra Wang 14772372
import search
import reverse
import aqi_sensors
import math
import time

class Error(Exception):
    pass

def direction(location:(float,float)):
    '''
    Given the lattitude and longitude of a location
    function checks if the values are positive or negative
    Then it returns the the values with the directions and omits the
    negative signs
    '''
    lat = location[0]
    lon = location[1]
    
    if lat < 0:
        lat  = abs(lat)
        lat_str = f'{lat}/S'
    else:
        lat_str = f'{lat}/N'

    if lon < 0:
        lon = abs(lon)
        lon_str = f'{lon}/W'
    else:
        lon_str = f'{lon}/E'

    return (lat_str, lon_str)

def print_final(final_list, center):
    '''
    given the final list and center, functions prints out everything in
    required format. 
    '''
    direction_center = direction(center)
    print(f'CENTER {direction_center[0]} {direction_center[1]}')
    for sensor in final_list:
        direction_sensor = direction(sensor[1])
        print(f'AQI {sensor[0]}')
        print(f'{direction_sensor[0]} {direction_sensor[1]}')
        print(sensor[2])


def user():
    '''
    Main function and calls all the other functions. 
    '''
    while True:
        try:
            center = input()
            range_miles= int(input()[len('RANGE'):])
            threshold = int(input()[len('THRESHOLD'):])
            max_num = int(input()[len('MAX'):])
            aqi =input()
            reverse_input = input()

            center = center_choose(center)
            sensor_list = aqi_choose(aqi,center,range_miles,threshold,max_num)
            final_list = reverse_choose(sensor_list, reverse_input, max_num)
            print_final(final_list, center)
            break

        except aqi_sensors.Error:
            break
        except reverse.Error:
            break
        except search.Error:
            break

def center_choose(center:str):
    '''
    Given center input from user, function creates either OnlineSearch object
    or FileSearch object and then calls center_function to grab data we are
    looking for. Finally, function returns data
    '''

    if 'CENTER NOMINATIM' in center:
        some_search = search.OnlineSearch(center[len('CENTER NOMINATIM '):])
        center = center_function(some_search)
        
    if 'CENTER FILE' in center:
        some_search = search.FileSearch(center[len('CENTER FILE '):])
        center = center_function(some_search)

    return center

def aqi_choose(aqi:str,center,range_miles,threshold,max_num):
    '''
    Given AQI input from user, function creates either OnlineAqiSensors object
    or FileAqiSensors object and then calls aqi_function to fetch the data
    we are looking for. Finally, function returns the data.
    '''
    if 'AQI PURPLEAIR' in aqi:
        some_aqi = aqi_sensors.OnlineAqiSensors()
        sensor_list = aqi_function(some_aqi,center,range_miles,threshold,max_num)
    if 'AQI FILE' in aqi:
        some_aqi = aqi_sensors.FileAqiSensors(aqi[len('AQI FILE '):])
        sensor_list = aqi_function(some_aqi,center,range_miles,threshold,max_num)

    return sensor_list

def reverse_choose(sensor_list:str, reverse_input:str,max_num:int):
    '''
    Given reverse input from user, function creates either OnlineReverse object
    or FileReverse object and then calls reverse_function to fetch the data
    we are looking for. Finally, function returns the data as a list.
    '''
    if 'REVERSE NOMINATIM' in reverse_input:
        reverse_input = reverse_input[len('REVERSE NOMINATUM '):]
        for sensor in sensor_list:
            rev = reverse.OnlineReverse(sensor[1])
            time.sleep(1)
            sensor.append(reverse_function(rev))
    
        return sensor_list
    
    if 'REVERSE FILES' in reverse_input:
        file_list= reverse_input[len('REVERSE FILES '):].split()
        for index in range(max_num):
            rev = reverse.FileReverse(file_list[index])
            sensor_list[index].append(reverse_function(rev))
        return sensor_list   

def center_function(search_object:object):
    '''
    given a center object (doesn't matter if it's a file or online),
    function calls the search_geo method inside their class and stores the
    data into a variable. Function then searches for the lattitude and
    longitude in the data and returns it

    '''
    data = search_object.search_geo()
    dictionary = data[0]
    lattitude = float(dictionary['lat'])
    longitude = float(dictionary['lon'])
    center = (lattitude,longitude)
    return center


def reverse_function(reverse_object:object):
    '''
    given a reverse object (either online or path) function calls the
    reverse_geo method in their class and then stores the data into a variable.
    Finally, function searches for data that contains display_name and
    returns it
    '''
    data = reverse_object.reverse_geo()
    place = data['display_name']
    return place

def distance_between(center, lat_lon:(float,float)):
    '''
    let dlat be the difference in the latitudes of the two points, in radians
    let dlon be the difference in the longitudes of the two points, in radians
    let alat be the average of the two latitudes, in radians
    let R be the radius of the Earth, in miles (3958.8)
    let x = dlon * cos(alat)
    let d = sqrt(x^2 + dlat^2) * R
    '''
    center_lat = center[0]
    center_lon = center[1]
    dlat = abs(center_lat - lat_lon[0])*(math.pi/180)
    dlon = abs(center_lon - lat_lon[1])*(math.pi/180)
    if dlon > math.pi:
        dlon = 2*math.pi-dlon 
    alat = ((center_lat + lat_lon[0])/2) * (math.pi/180)
    R = 3958.8
    x = dlon * math.cos(alat)
    d = math.sqrt((x*x) + (dlat*dlat)) * R
    return d

def aqi_value(pm:float):
    '''
    given a pm concentration, returns the correct AQI value
    '''
    if 0.0 <= pm <12.1:
        lowest =0
        proportion= (pm-0.0)/(12.0)
        num = proportion*(50-0)
        value = lowest + num 
    if 12.1 <= pm < 35.5:
        lowest = 51
        proportion = (pm-12.1)/(35.4-12.1)
        num = proportion*(100-51)
        value = lowest + num
    if 35.5 <= pm < 55.5:
        lowest = 101
        proportion = (pm-35.5)/(55.4-35.5)
        num = proportion*(150-101)
        value = lowest + num
    if 55.5<= pm< 150.5:
        lowest = 151
        proportion = (pm-55.5)/(150.4-55.5)
        num = proportion*(200-151)
        value = lowest + num
    if 150.5<= pm < 250.5:
        lowest = 201
        proportion = (pm-150.5)/(250.4-150.5)
        num = proportion*(300-201)
        value = lowest + num
    if 250.5<= pm < 350.5:
        lowest = 301
        proportion = (pm-250.5)/(350.4-250.5)
        num = proportion*(400-301)
        value = lowest + num
    if 350.5<= pm < 500.5:
        lowest = 401
        proportion = (pm-350.5)/(500.4-350.5)
        num = proportion*(500-401)
        value = lowest + num
    if pm >= 500.5:
        value = 501

    return round(value)

def aqi_function(aqi_object:object,
                 center:(float,float),
                 range_miles:int,
                 threshold:int,
                 max_num:int):
    '''
    Given an aqi object, calls the sensors_data method in their class
    and stores the data into a variable. Function then returns a list
    of the sensors found in the data that is 1) in range 2) is over or at
    threshold 3) is outdoors 4) has reported in the lsat hour 
    '''
    data = aqi_object.sensors_data()
    fields = data['fields']
    pm_index = fields.index('pm')
    age_index = fields.index('age')
    typ_index = fields.index('Type')
    lat_index = fields.index('Lat')
    lon_index = fields.index('Lon')


    list_sensors=[]
    for sensor in data['data']:
        '''
        1) In range
        2) IS AT or OVER threshold
        3) Type  = 0
        4) has reported in last hour (age is not an hour or more)
        '''
        lat = sensor[lat_index]
        lon = sensor[lon_index]
        typ = sensor[typ_index]
        age = sensor[age_index]
        pm  = sensor[pm_index]
        
        if lat!= None and lon!= None and typ!= None and age!= None and pm!=None:
            aqi_pm = aqi_value(pm)
            if distance_between(center,(lat,lon)) <= range_miles and typ ==0 and age<=3600 and aqi_pm >= threshold:
                list_sensors.append([aqi_pm,(lat,lon)])

    
    sensors = sorted(list_sensors,reverse=True)
    if len(sensors) > max_num:
        sensors = sensors[:max_num]
    return sensors 
        
                      
                                             
                                                  
if __name__ == '__main__':
    user()
