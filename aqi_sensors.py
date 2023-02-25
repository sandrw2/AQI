#Sandra Wang 14772372
import json
import urllib.request
import urllib.error
from pathlib import Path

def _expected_sensors(data: dict)-> bool:
    '''
    checks if data is in the expected format and if these
    fields exists. If these fields exists, returns True.
    '''
    try:
        fields = data['fields']
        data_collection = data['data']
        fields.index('pm')
        fields.index('age')
        fields.index('Type')
        fields.index('Lat')
        fields.index('Lon')
            
        return True
    except TypeError:
        return False
    except KeyError:
        return False
    except ValueError:
        return False
    except IndexError:
        return False

class Error(Exception):
    pass

class OnlineAqiSensors:
    def __init__(self):
        pass
    def sensors_data(self):
        '''
        requests data from purpleair then returns the data. If exceptions
        occur, function  catches thme and then prints corresponding error
        message
        '''
        url = 'https://www.purpleair.com/data.json'
        response = None
        try:
            request = urllib.request.Request(url) 
            response = urllib.request.urlopen(request)
            json_text = response.read()
            response.close()
            jeson_text = json_text.decode(encoding = 'utf-8')
            data = json.loads(json_text)
            
            if _expected_sensors(data):
                return data
            else:
                print('FAILED')
                print(f'{response.status} {url}')
                print('FORMAT')
                raise Error
            
        
        except urllib.error.HTTPError as e:
            print('FAILED')
            print(f'{e.code} {url}')
            print('NOT 200')
            raise Error
        except urllib.error.URLError:
            print('FAILED')
            print(url)
            print('NETWORK')
            raise Error
        except ValueError:
            print('FAILED')
            print(f'{response.status} {url}')
            print('FORMAT')
            raise Error

        finally:
            if response!= None:
                response.close()

                
class FileAqiSensors:
    def __init__(self, path: 'path'):
        self._path = path

    def sensors_data(self):
        '''
        Using the path object, function fetches data from the file and
        returns it. If exceptions occur then function catches them and
        returns the corresponding error message. 
        '''
        the_file = None
       
        try:
            the_file = open(Path(self._path), 'r')
            the_string = the_file.read()
            data = json.loads(the_string)

            if _expected_sensors(data):
               return data
            else:
                print('FAILED')
                print(self._path)
                print('FORMAT')
                raise Error
            

        except FileNotFoundError:
            print('FAILED')
            print(self._path)
            print('MISSING')
            raise Error
        except OSError:
            print('FAILED')
            print(self._path)
            print('MISSING')
            raise Error
        except ValueError:
            print('FAILED')
            print(self._path)
            print('FORMAT')
            raise Error
        finally:
            if the_file != None:
                the_file.close()

    
            

